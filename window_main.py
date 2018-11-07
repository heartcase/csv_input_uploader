# -*- coding:utf-8 -*-
# Main Window of the Application
# 主窗口
# By Heart Case
#
import PySimpleGUI as sg


def create_main_windows():
    # 初始化窗口
    window = sg.Window('CSV uploader', no_titlebar=True, grab_anywhere=True)
    _window_show = window.Show

    # 愚蠢的 丑陋的 设置默认窗口大小的方法
    def _new_window_show(non_blocking=False):
        for each in window.Rows[3:].copy():
            if each[0].Key == 'PLACE_HOLDER':
                window.Rows.remove(each)
                break
        if len(window.Rows) < 10:
            place_holder = sg.Text('', key='PLACE_HOLDER', size=(0, 10 - len(window.Rows)))
            window.Rows.append([place_holder])
        _window_show(non_blocking)
    window.Show = _new_window_show
    # Row 0: Menu
    # 设置菜单布局
    menu_layout = [
        ['File', ['Config', 'Exit']]
    ]
    menu = sg.Menu(menu_layout, background_color='#FFFFFF')
    # Row 1: Post
    files_selector = sg.FilesBrowse('添加文件', key='ADD_FILES', target=(None, None), size=(12, 1))
    _selector_callback = files_selector.ButtonCallBack

    # 拦截按钮回调
    def _new_selector_callback():
        files_selector.Update(disabled=True)
        _selector_callback()
        files = files_selector.TKStringVar.get().split(';')
        for each in files:
            if each != '':
                add_task(each)
        window.LastButtonClicked = files_selector.Key
        window.TKroot.quit()

    files_selector.ButtonCallBack = _new_selector_callback
    # Row 2: Task List Label
    tasks_msg = sg.Text('任务列表', size=(46, 1))
    # Row 3... Task Lists

    def add_task(filename):
        # 跳过重复文件
        if any(['REMOVE_' + filename == each[3].Key for each in window.Rows[3:] if len(each) > 2]):
            return
        # 创建删除文件按钮
        remove_button = sg.Button('删除', change_submits=True, size=(5, 1), button_color=('#FFFFFF', '#FF0000'))
        remove_button.Key = 'REMOVE_' + filename
        _button_callback = remove_button.ButtonCallBack

        # 重写按钮回调方法
        def _new_button_callback():
            _button_callback()
            for each in window.Rows[3:].copy():
                if each[3].Key == remove_button.Key:
                    window.Rows.remove(each)
                    break
        remove_button.ButtonCallBack = _new_button_callback
        # 开始/暂停/恢复按钮
        start_pause_resume_button = sg.Button('开始', change_submits=False,
                                              size=(5, 1), button_color=('#FFFFFF', '#66CC66'))
        start_pause_resume_button.Key = 'START_' + filename
        # 添加新行
        window.Rows.append([
            sg.Text('上传 ' + filename.split('/')[-1], size=(20, 1), background_color='#FFFFFF'
                    ), sg.ProgressBar(100, size=(25, 18)), start_pause_resume_button, remove_button
        ])

    # 设置布局
    layout = [
        [menu],
        [tasks_msg, files_selector],
        []
    ]
    window.Layout(layout)
    return window

