# -*- coding: utf-8 -*-
# Ftp connection methods
# FTP 连接方法
# By Heart Case
from ftplib import FTP
import os


def upload_progress(local_file_path, ftp_file_path, ftp, bar, flag):
    if flag['stop']:
        raise Exception('用户中断')
    else:
        bar.UpdateBar(
            100 * int(ftp.sendcmd('SIZE ' + ftp_file_path).split(' ')[1]) / os.path.getsize(local_file_path)
        )


def upload_file(local_file_path,
                ftp_file_path,
                ftp,
                callback=None,
                rest=False,
                ):
    try:
        if rest:
            size = int(ftp.sendcmd('SIZE ' + ftp_file_path).split(' ')[1])
            file = open(local_file_path, 'rb')
            file.seek(size)
            ftp.sendcmd('REST ' + str(size))
            ftp.storbinary('STOR ' + ftp_file_path, file, callback=callback, rest=size)
            file.close()
        else:
            file = open(local_file_path, 'rb')
            ftp.storbinary('STOR ' + ftp_file_path, file, callback=callback)
    except Exception as e:
        print(e)