# -*- coding:utf-8 -*-
from ftplib import FTP
from configparser import ConfigParser
from windows.window_main import window as main_window
from windows.uploading_bar import create_progress_bar
import os
from threading import Thread

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

BLOCK_SIZE = 8192


def counter_inc(_):
    global counter
    counter += BLOCK_SIZE



while 1:
    event, values = main_window.Read()
    file_list = values['files'].split(';') if values['files'] else []
    main_window.FindElement('list').Update(values=file_list)
    if event == 'Submit' and len(file_list):
        main_window.Hide()
        main_window.FindElement('list').Update(values=[])
        for index, each in enumerate(file_list):
            totalSize = os.path.getsize(each)
            filename = each.split('/')[-1]
            msg = 'Uploading: ' + filename + ' (' + str(index) + '/' + str(len(file_list)) + ')'
            with create_progress_bar(msg) as progress_window:
                progress_bar = progress_window.FindElement('progressbar')
                counter = 0
                with open(each, 'rb') as file:
                    t = Thread(target=ftp.storbinary, args=[
                        'STOR ' + filename,
                        file,
                        BLOCK_SIZE,
                        counter_inc
                    ])
                    t.start()
                    while 1:
                        event, values = progress_window.Read(timeout=0)
                        p = int(counter / totalSize * 10000)
                        progress_bar.UpdateBar(p)
                        if not t.isAlive():
                            progress_window.Close()
                            break
        main_window.Show()
