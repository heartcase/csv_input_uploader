# -*- coding: utf-8 -*-
from ftp_connections import upload_file, upload_progress
from PySimpleGUI import Window, ProgressBar, Button
from ftplib import FTP
from threading import Thread
from time import sleep

local_path = 'D:\\ftp\\input\\3743.csv'
ftp_path = '3743.csv'
ftp_host = 'localhost'
ftp_user = 'boyang'
ftp_password = 'abcdefg'

bar = ProgressBar(100)
flag = {
    'stop': False,
    'start': True
}
window = Window('My show')
window.Layout(
    [
        [bar],
        [Button('OK')]
    ]
)
window.Read(timeout=0)
start = True

ftp = FTP(ftp_host)
ftp.login(ftp_user, ftp_password)

t = Thread(
    target=upload_file,
    args=(
        local_path,
        ftp_path,
        ftp,
        flag,
        lambda x: upload_progress(local_path, ftp_path, ftp, bar),
        False
    )
)

t.start()
while 1:
    window.Read()
    flag['stop'] = not flag['stop']
    t.join()
    if not flag['stop']:
        ftp = FTP(ftp_host)
        ftp.login(ftp_user, ftp_password)
        t = Thread(
            target=upload_file,
            args=(
                local_path,
                ftp_path,
                ftp,
                flag,
                lambda x: upload_progress(local_path, ftp_path, ftp, bar),
                True
            )
        )
        t.start()

window.Close()

ftp.close()