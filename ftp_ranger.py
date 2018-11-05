# -*- coding:utf-8 -*-
from ftplib import FTP
from configparser import ConfigParser
from windows.window_main import create_main_windows
from windows.uploading_bar import create_progress_bar
from windows.login_window import create_login_window
import os
from threading import Thread
import requests
import hashlib
import json
import pandas as pd

ftp_config_path = 'ftp_config.ini'

config = ConfigParser()
config.read(ftp_config_path)
ftp_server = config['ftp_server']
ftp_host = ftp_server['host']
ftp_port = ftp_server['port']
ftp_user = ftp_server['user']
ftp_password = ftp_server['password']
ftp = FTP(host=ftp_host)
ftp.login(user=ftp_user, passwd=ftp_password)
login_server = config['login_server']
login_host = login_server['host']
login_port = login_server['port']
task_server = config['task_server']
task_host = task_server['host']
task_port = task_server['port']

username = ''

BLOCK_SIZE = 8192
USE_MOCK = True

counter = 0
is_login = False
token = ''
msg = 'Greeting: Welcome, cowboy!'


def login():
    global is_login, token, msg, username
    with create_login_window(msg) as login_window:
        event, values = login_window.Read()
        if event is None:
            exit(0)
        try:
            password = hashlib.md5((values['password'] + 'salt').encode()).hexdigest()
            url = 'http://' + login_host + ':' + login_port + '/login'
            response = requests.post(url, auth=(values['user'], password))
            username = values['user']
        except TypeError:
            msg = 'Bad Bad Inputs'
            return
        except requests.exceptions.ConnectionError:
            if USE_MOCK:
                is_login = True
                login_window.Close()
                return
            else:
                msg = 'Error: Remote Server No Response, Access Failure.'
                login_window.Close()
                return
        else:
            content = json.loads(response.content.decode())
            if content['code'] == 20000:
                is_login = True
                token = content['data']['token']
            else:
                msg = 'Error: Identity Mismatched, Login Denied'
        login_window.Close()


def counter_inc(_):
    global counter
    counter += BLOCK_SIZE


def counter_rst():
    global counter
    counter = 0


def sub_loop(file_list, task_type):
    global msg, is_login
    url = 'http://' + task_host + ':' + task_port + '/file'
    for index, each in enumerate(file_list):
        total_size = os.path.getsize(each)
        filename = each.split('/')[-1]
        url = 'http://' + task_host + ':' + task_port + '/file'
        headers = {"Authorization": "Bearer " + token}
        payload = {
            "filename": filename,
            'owner': username,
            'file_size': total_size,
            'task_type': task_type
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
        except requests.exceptions.ConnectionError:
            if USE_MOCK:
                pass
            else:
                msg = 'File Register Server Access Failure'
                return
        else:
            content = json.loads(response.content.decode())
            if content['code'] != 20000:
                msg = 'Error: Identity Mismatched, Login Denied'
                is_login = False
                return

    for index, each in enumerate(file_list):
        total_size = os.path.getsize(each)
        filename = each.split('/')[-1]
        msg = 'Uploading: ' + filename + ' (' + str(index + 1) + '/' + str(len(file_list)) + ')'
        with create_progress_bar(msg) as progress_window:
            progress_bar = progress_window.FindElement('progressbar')
            counter_rst()
            with open(each, 'rb') as file:
                t = Thread(target=ftp.storbinary, args=['STOR ' + filename, file, BLOCK_SIZE, counter_inc])
                t.start()
                while 1:
                    progress_window.Read(timeout=0)
                    p = int(counter / total_size * 10000)
                    progress_bar.UpdateBar(p)
                    if not t.isAlive():
                        break
            progress_window.Close()
            payload = {
                "filename": filename,
                'status': 'finished'
            }
            try:
                requests.put(url, data=payload)
            except requests.exceptions.ConnectionError:
                pass
    msg = str(len(file_list)) + ' file(s) have been uploaded.'


def check_data_format(file_list, task_type):
    global msg, is_login
    url = 'http://' + task_host + ':' + task_port + '/task' + '?task_type=' + task_type
    headers = {"Authorization": "Bearer " + token}
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        if USE_MOCK:
            if task_type == 'Task_1':
                data_format = ['col1', 'col2', 'col3', 'col4']
            else:
                data_format = ['col1', 'col2', 'col3', 'col20']
        else:
            msg = 'Error: Remote Server No Response, Access Failure.'
            is_login = False
            return False
    else:
        content = json.loads(response.content.decode())
        if content['code'] == 20000:
            data_format = content['data']['data_format']
        else:
            msg = 'Error: Passport expired.'
            is_login = False
            return False

    return all([
            all([
                col in pd.read_csv(file, nrows=1).columns
                for col in data_format
            ])
            for file in file_list
        ])


def main_loop():
    global msg
    while not is_login:
        login()
    file_list = []
    with create_main_windows(msg) as main_window:
        while 1:
            main_window.Read(timeout=0)
            try:
                main_window.FindElement('list').Update(values=file_list)
            except Exception as e:
                print(e)
                return False
            event, values = main_window.Read()
            if event is None:
                exit(0)
            file_list = values['files'].split(';') if values['files'] else []
            if event == 'files':
                continue
            if event == 'Submit' and len(file_list):
                if values['check']:
                    if not check_data_format(file_list, values['task']):
                        msg = 'Some Input Files Have Bad Format, Check Column Names Again!'
                        continue
                break
        main_window.Close()
    sub_loop(file_list, values['task'])
    return True


while 1:
    main_loop()
