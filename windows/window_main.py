# -*- coding:utf-8 -*-
import PySimpleGUI as sg


def create_main_windows(msg):
    message_text = sg.Text(msg)
    type_label = sg.Text('Task Type')
    type_selector = sg.Combo(['Task_1', 'Task_2'], readonly=True, key='task')
    type_checker = sg.Checkbox('Check Data Format', True, key='check')
    files_label = sg.Text('Select Input Files')
    files_selector = sg.FilesBrowse('Select Files', key='files', change_submits=True)
    files_selector.FileTypes = [("CSV Files", "*.csv")]
    files_selector.Target = 'files'
    files_previews = sg.Listbox(values=[], key='list', size=(100, 6))
    submit_button = sg.Button('Submit')
    layout = [
        [message_text],
        [type_label, type_selector, type_checker],
        [files_label, files_selector],
        [files_previews],
        [submit_button]
    ]
    return sg.Window('CSV INPUT UPLOADER Ver 0.2').Layout(layout)
