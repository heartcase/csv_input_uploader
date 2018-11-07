# -*- coding: utf-8 -*-
# Simple Ftp Uploader with Graphical Interface
# 简易FTP上传工具
# By Heart Case
from read_config import read_config
from window_main import create_main_windows

# region Constants
# 配置文件路径
CONFIG_PATH = 'config.ini'
# 读取配置文件
CONFIG = read_config(CONFIG_PATH)
# FTP服务器配置
FTP_SERVER = CONFIG['ftp_server']
# 客户端配置
CLIENT = CONFIG['client']
# FTP主机地址
FTP_HOST = FTP_SERVER['host']
# FTP 端口地址
FTP_PORT = FTP_SERVER['port']
# FTP 用户名
FTP_USER = FTP_SERVER['user']
# FTP 密码
FTP_PASSWORD = FTP_SERVER['password']
# 上传数据块大小
BLOCK_SIZE = CLIENT['block_size']
# endregion

# region Global Variables
# ftp已连接
ftp_connected = False
# 授权服务器登陆
is_login = False
# 用户名
username = ''
# 密码
password = ''
# Json Web Token
token = ''
# 程序状态
state = 'MAIN'
# 触发事件
event = None
# 状态值
values = None
# endregion

# region Window instances initialization
main_window = create_main_windows()
# endregion


# region Finite State Machine
def state_main():
    global state, event, values
    event, values = main_window.Read()
    if event == 'ADD_FILES' or event[0:6] == 'REMOVE':
        main_window.Location = main_window.CurrentLocation()
        main_window.Close()
        main_window.Show(non_blocking=True)
    state = 'MAIN'


state_functions = {
    'MAIN': state_main
}

# endregion

while 1:
    state_functions[state]()
