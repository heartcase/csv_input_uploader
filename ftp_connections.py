# -*- coding: utf-8 -*-
# Ftp connection methods
# FTP 连接方法
# By Heart Case
from ftplib import FTP
import os


def upload_progress(local_file_path, ftp_file_path, ftp, bar, flag):
    ftp_size = ftp.size(ftp_file_path)
    target_size = os.path.getsize(local_file_path)
    flag['done'] = ftp_size == target_size
    bar.UpdateBar(
        100 * ftp_size // target_size
    )


def upload_file(local_file_path,
                ftp_file_path,
                ftp,
                flag,
                callback=None,
                rest=False,
                done_callback=None
                ):
    try:
        if rest:
            size = int(ftp.sendcmd('SIZE ' + ftp_file_path).split(' ')[1])
            file = open(local_file_path, 'rb')
            file.seek(size)
            ftp.sendcmd('REST ' + str(size))
            ftp.voidcmd('TYPE I')
            with ftp.transfercmd('STOR ' + ftp_file_path, 0) as conn:
                while 1:
                    buf = file.read(8192)
                    if not buf:
                        break
                    conn.sendall(buf)
                    if flag['stop']:
                        ftp.abort()
                        file.close()
                        break
                    if callback:
                        callback(buf)
            ftp.voidresp()
            file.close()
        else:
            file = open(local_file_path, 'rb')
            ftp.voidcmd('TYPE I')
            with ftp.transfercmd('STOR ' + ftp_file_path, 0) as conn:
                while 1:
                    buf = file.read(8192)
                    if not buf:
                        break
                    conn.sendall(buf)
                    if flag['stop']:
                        ftp.abort()
                        file.close()
                        break
                    if callback:
                        callback(buf)
            ftp.voidresp()
            file.close()
        if done_callback and flag['done']:
            done_callback()
    except Exception as e:
        print(e)