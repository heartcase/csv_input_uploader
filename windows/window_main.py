# -*- coding:utf-8 -*-
import PySimpleGUI as sg


def create_main_windows():
    type_label = sg.Text('Task Type')
    type_selector = sg.Combo(['Task_1', 'Task_2'], readonly=False, key='hello', change_submits=True)

    files_label = sg.Text('Select Input Files')
    files_selector = sg.FilesBrowse('Select Files', key='files')
    files_selector.Target = 'files'
    files_selector.ChangeSubmits = True
    files_previews = sg.Listbox(values=[], key='list', size=(100, 6))
    submit_button = sg.Button('Submit')
    layout = [
        [type_label, type_selector],
        [files_label, files_selector],
        [files_previews],
        [submit_button]
    ]
    return sg.Window('CSV INPUT UPLOADER Ver 0.1').Layout(layout)
