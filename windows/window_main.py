# -*- coding:utf-8 -*-
import PySimpleGUI as sg
from configparser import ConfigParser, SectionProxy

ftp_config_path = 'ftp_config.ini'
config = ConfigParser()
config.read(ftp_config_path)
file_types = list(config['file_types'].values())


def create_main_windows(msg):
    message_text = sg.Text(msg)
    type_label = sg.Text('File Type')
    type_selector = sg.Combo(file_types, readonly=True, key='task')
    type_checker = sg.Checkbox('Check Data Format', False, key='check', disabled=True)
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
