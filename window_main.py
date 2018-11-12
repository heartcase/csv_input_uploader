# -*- coding:utf-8 -*-
# Main Window of the Application
# 主窗口
# By Heart Case
#
from read_config import CONFIG
from ftplib import FTP
from PySimpleGUI import Button, ProgressBar, Text, Popup, Window, Menu, FilesBrowse, Multiline
from threading import Thread
from ftp_connections import upload_file, upload_progress
# Constants
MIN_ROWS = 15
REMOVE_BUTTON_COLUMN = 3
START_BUTTON_COLUMN = 2
# FTP服务器配置
FTP_SERVER = CONFIG['ftp_server']
# 客户端配置
CLIENT = CONFIG['client']
# FTP主机地址
FTP_HOST = FTP_SERVER['host']
# FTP 用户名
FTP_USER = FTP_SERVER['user']
# FTP 密码
FTP_PASSWORD = FTP_SERVER['password']


def create_ftp_thread(local_path, ftp_path, flag, bar, rest, remove_button):
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASSWORD)
    return Thread(
        target=upload_file,
        args=(
            local_path,
            ftp_path,
            ftp,
            flag,
            lambda x: upload_progress(local_path, ftp_path, ftp, bar, flag),
            rest,
            remove_button.ButtonCallBack
        ),
        daemon=True,
    )


def create_menu():
    """
    创建菜单
    :return: 菜单对象
    """
    menu_layout = [
        ['文件', ['配置', '---', '全部开始', '全部删除', '---', '退出']]
    ]
    return Menu(menu_layout, background_color='#FFFFFF')


def create_remove_button(filename, window):
    remove_button = Button('删除', change_submits=False, size=(5, 1), button_color=('#FFFFFF', '#FF0000'))
    remove_button.Key = 'REMOVE_' + filename
    _button_callback = remove_button.ButtonCallBack

    # 重写按钮回调方法
    def _new_button_callback():
        _button_callback()
        for each in window.Rows[3:].copy():
            if len(each) > REMOVE_BUTTON_COLUMN and each[REMOVE_BUTTON_COLUMN].Key == remove_button.Key:
                if each[START_BUTTON_COLUMN].Key[:5] == 'PAUSE':
                    each[START_BUTTON_COLUMN].ButtonCallBack()
                window.Rows.remove(each)
                break
        window.LastButtonClicked = remove_button.Key
        window.TKroot.quit()

    remove_button.ButtonCallBack = _new_button_callback
    return remove_button


def create_start_button(filename, window):
    start_button = Button('开始', change_submits=False,
                             size=(5, 1), button_color=('#FFFFFF', '#66CC66'))
    start_button.Key = 'START_' + filename
    _button_callback = start_button.ButtonCallBack
    flag = {'stop': True,
            'started': False,
            'done': False}

    # 重写按钮回调方法
    def _new_button_callback():
        flag['stop'] = not flag['stop']
        _button_callback()
        if start_button.Key[0:5] == 'START':
            remove_button = window.FindElement('REMOVE_' + filename)
            bar = window.FindElement('PROGRESS_' + filename)
            if flag['started']:
                create_ftp_thread(filename, filename.split('/')[-1], flag, bar, True, remove_button).start()
            else:
                flag['started'] = True
                create_ftp_thread(filename, filename.split('/')[-1], flag, bar, False, remove_button).start()
            start_button.Update(text='暂停', button_color=('#FFFFFF', '#AAAA88'))
            start_button.Key = 'PAUSE_' + start_button.Key[6:]
        else:
            start_button.Update(text='开始', button_color=('#FFFFFF', '#66CC66'))
            start_button.Key = 'START_' + start_button.Key[6:]
        window.Refresh()

    start_button.ButtonCallBack = _new_button_callback
    return start_button


def add_task(filename, window):
        # 跳过重复文件
        if any(['REMOVE_' + filename == each[REMOVE_BUTTON_COLUMN].Key for each in window.Rows[3:] if len(each) > 2]):
            return
        # 创建删除文件按钮
        remove_button = create_remove_button(filename, window)
        # 开始/暂停/恢复按钮
        start_button = create_start_button(filename, window)
        # 进度条
        progress_bar = ProgressBar(100, size=(25, 18), key='PROGRESS_' + filename)
        # 添加新行
        window.Rows.insert(-1, [
            Text('上传 ' + filename.split('/')[-1], size=(20, 1), background_color='#FFFFFF'),
            progress_bar,
            start_button,
            remove_button
        ])


def create_files_browser(window):
    """
    创建文件选择按钮
    :return:
    """
    files_selector = FilesBrowse('添加文件', key='ADD_FILES', target=(None, None), size=(10, 1))
    files_selector.FileTypes = [("CSV Files", "*.csv")]
    _selector_callback = files_selector.ButtonCallBack

    # 拦截按钮回调
    def _new_selector_callback():
        files_selector.Update(disabled=True)
        _selector_callback()
        files = files_selector.TKStringVar.get().split(';')
        for each in files:
            if each == '':
                break
            if len(window.Rows) < MIN_ROWS:
                add_task(each, window)
            else:
                window.Hide()
                Popup('提示', '无法添加更多任务!', keep_on_top=True)
                break
        window.LastButtonClicked = files_selector.Key
        window.TKroot.quit()

    files_selector.ButtonCallBack = _new_selector_callback
    return files_selector


def create_start_all_button(window):
    start_all_button = Button('全部开始', change_submits=False, size=(10, 1), button_color=('#FFFFFF', '#66CC66'))
    start_all_button.Key = 'START_ALL'

    _button_callback = start_all_button.ButtonCallBack

    # 重写按钮回调方法
    def _new_button_callback():
        _button_callback()
        for each in window.Rows[3:]:
            if len(each) > START_BUTTON_COLUMN and each[START_BUTTON_COLUMN].Key[0:5] == 'START':
                each[START_BUTTON_COLUMN].ButtonCallBack()
        window.Refresh()

    start_all_button.ButtonCallBack = _new_button_callback
    return start_all_button


def create_remove_all_button(window):
    remove_all_button = Button('全部删除', change_submits=False, size=(10, 1), button_color=('#FFFFFF', '#FF0000'))
    remove_all_button.Key = 'REMOVE_ALL'
    _button_callback = remove_all_button.ButtonCallBack

    # 重写按钮回调方法
    def _new_button_callback():
        _button_callback()
        for each in window.Rows[3:]:
            if len(each) > REMOVE_BUTTON_COLUMN and each[START_BUTTON_COLUMN].Key[:5] == 'PAUSE':
                each[START_BUTTON_COLUMN].ButtonCallBack()
        window.Rows = window.Rows[:3] + [window.Rows[-1]]
        window.TKroot.quit()

    remove_all_button.ButtonCallBack = _new_button_callback
    return remove_all_button


def create_pause_all_button(window):
    pause_all_button = Button('全部暂停', change_submits=False, size=(10, 1), button_color=('#FFFFFF', '#AAAA88'))
    pause_all_button.Key = 'PAUSE_ALL'
    _button_callback = pause_all_button.ButtonCallBack

    # 重写按钮回调方法
    def _new_button_callback():
        _button_callback()
        for each in window.Rows[3:]:
            if len(each) > START_BUTTON_COLUMN and each[START_BUTTON_COLUMN].Key[0:5] == 'PAUSE':
                each[START_BUTTON_COLUMN].ButtonCallBack()
        window.Refresh()

    pause_all_button.ButtonCallBack = _new_button_callback
    return pause_all_button


def create_main_windows():
    """
    创建主要窗口
    :return: 主窗口对象
    """
    # 初始化窗口
    window = Window('CSV uploader')
    _window_show = window.Show

    # 愚蠢的 丑陋的 设置默认窗口大小的方法
    def _new_window_show(non_blocking=False):
        for each in window.Rows[3:].copy():
            if each[0].Key == 'PLACE_HOLDER':
                window.Rows.remove(each)
                break
        if len(window.Rows) < MIN_ROWS:
            place_holder = Text('', key='PLACE_HOLDER', size=(0, MIN_ROWS - len(window.Rows)))
            window.Rows.insert(-1, [place_holder])
        _window_show(non_blocking)
    window.Show = _new_window_show

    # Row 0: Menu
    # 设置菜单布局
    menu = create_menu()
    # Row 1: Post, Start All, Pause All, Remove All
    files_selector = create_files_browser(window)
    start_all_button = create_start_all_button(window)
    remove_all_button = create_remove_all_button(window)
    pause_all_button = create_pause_all_button(window)

    # Row 2: Task List Label
    tasks_msg = Text('任务列表', size=(12, 1))
    # Row -1: Output
    output = Multiline(size=(70, 5))
    # 设置布局
    layout = [
        [menu],
        [tasks_msg, files_selector, start_all_button, pause_all_button, remove_all_button],
        [],
        [output]
    ]
    window.Layout(layout)
    return window

