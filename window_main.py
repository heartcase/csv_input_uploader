# -*- coding:utf-8 -*-
# Main Window of the Application
# 主窗口
# By Heart Case
#
import PySimpleGUI as sg


def create_main_windows():
    # 初始化窗口
    window = sg.Window('CSV uploader', no_titlebar=True, grab_anywhere=True)
    # Row 0: Menu
    menu_layout = [
        ['File', ['Config', 'Exit']]
    ]
    menu = sg.Menu(menu_layout)
    # Row 1: Post
    files_selector = sg.FilesBrowse('选择文件', key='FILE', change_submits=True)
    _selector_callback = files_selector.ButtonCallBack

    def _new_selector_callback():
        _selector_callback()
        files = files_selector.TKStringVar.get().split(';')
        for each in files:
            add_task(each)

    files_selector.ButtonCallBack = _new_selector_callback
    # Row 2: Task List Label
    tasks_msg = sg.Text('任务列表')
    # Row 3... Task Lists

    def add_task(filename):
        remove_button = sg.Button('删除任务', change_submits=True, size=(10, 1))
        remove_button.Key = 'REMOVE_' + filename
        window.Rows.append([
            sg.Text('上传 ' + filename.split('/')[-1], size=(20, 1)), sg.ProgressBar(100, size=(25, 1)), remove_button
        ])

    task_layout = [
        [files_selector]
    ]
    # Row -1 Remove Button
    # remove_button = sg.Button('删除任务', key='REMOVE', change_submits=True, size=(10, 1))

    lay_out = [
        [menu],
        [tasks_msg],
        *task_layout,
    ]
    window.Layout(lay_out)
    return window

