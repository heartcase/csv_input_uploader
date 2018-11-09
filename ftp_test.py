# -*- coding: utf-8 -*-
from ftp_connections import upload_file, upload_progress
from PySimpleGUI import Window, ProgressBar, Button
from ftplib import FTP
from threading import Thread

local_path = ''
ftp_path = ''
ftp_host = 'localhost'
ftp_user = 'boyang'
ftp_password = 'abcdefg'
ftp = FTP(ftp_host)
ftp.login(ftp_user, ftp_password)
bar = ProgressBar(100)
flag = {
    'stop': False
}
window = Window('My show')
window.Layout(
    [
        [bar],
        [Button('OK')]
    ]
)
window.Read(timeout=0)
t = Thread(
    target=upload_file,
    args=(
        local_path,
        ftp_path,
        ftp,
        lambda x: upload_progress(local_path, ftp_path, ftp, bar, flag),
        False
    )
)
t.setDaemon(True)
t.start()
window.Read()
window.Close()
flag['stop'] = True
ftp.close()