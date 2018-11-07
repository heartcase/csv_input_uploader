# -*- coding: utf-8 -*-
# Read Configs Or Create One If The File Does Not Exist
# 读取配置文件 或创建新的配置文件
# By Heart Case
from configparser import ConfigParser
import os


def read_config(config_path):
    """
    从指定路径读取配置文件
    :param config_path: 配置文件路径
    :return: config 对象
    """
    config = ConfigParser()
    # 判断路径是否存在
    if not os.path.exists(config_path):
        # 创建配置Section
        config.add_section('ftp_server')
        config.add_section('client')
        config.add_section('file')
        # 创建默认配置项
        config.set('ftp_server', 'host', 'localhost')
        config.set('ftp_server', 'port', '21')
        config.set('ftp_server', 'user', 'admin')
        config.set('ftp_server', 'password', 'password')
        config.set('client', 'block_size', '8192')
        config.set('client', 'path', '/')
        # 写入配置文件
        config.write(open(config_path, 'w'))
    else:
        # 读取config 文件
        config.read(config_path)
    return config
