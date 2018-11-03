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

BLOCK_SIZE = 8192

counter = 0
is_login = False
token = ''
msg = 'Greeting: Welcome, cowboy!'


def login():
    global is_login, token, msg
    with create_login_window(msg) as login_window:
        event, values = login_window.Read()
        password = hashlib.md5((values['password'] + 'salt').encode()).hexdigest()
        try:
            url = 'http://' + login_host + ':' + login_port + '/login'
            response = requests.post(url, auth=(values['user'], password))
        except:
            msg = 'Error: Remote Server No Response, Access Failure.'
            login_window.Close()
            return
        content = json.loads(response.content.decode())
        if content['code'] == 20000:
            is_login = True
            token = content['data']['token']
            msg = 'Greeting: Welcome, cowboy!'
        else:
            msg = 'Error: Identity Mismatched, Login Denied'
        login_window.Close()


def counter_inc(_):
    global counter
    counter += BLOCK_SIZE


def counter_rst():
    global counter
    counter = 0


def sub_loop(file_list):
    global msg
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
                        progress_window.Close()
                        break



def main_loop():
    while not is_login:
        login()
    file_list = []
    with create_main_windows() as main_window:
        while 1:
            main_window.Read(timeout=0)
            try:
                main_window.FindElement('list').Update(values=file_list)
            except:
                return False
            event, values = main_window.Read()
            file_list = values['files'].split(';') if values['files'] else []
            if event == 'Submit' and len(file_list):
                break
        main_window.Close()
    sub_loop(file_list)
    return True


while main_loop():
    pass
