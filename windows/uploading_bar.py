# -*- coding:utf-8 -*-
import PySimpleGUI as sg


def create_progress_bar(msg):
    progress_msg = sg.Text(msg, key='msg')
    progress_info = sg.Text('Waiting...', key='info')
    progress_bar = sg.ProgressBar(10001, orientation='h', size=(20, 20), key='progressbar')
    progress_pause = sg.Button('Pause')
    progress_cancel = sg.Button('Cancel')
    layout = [[progress_msg],
              [progress_info],
              [progress_bar],
              [progress_pause, progress_cancel]]

    return sg.Window('Custom Progress Meter', no_titlebar=True).Layout(layout)



