# -*- coding:utf-8 -*-
import PySimpleGUI as sg


def create_progress_bar(msg):
    progress_msg = sg.Text(msg, key='msg')
    layout = [[progress_msg],
              [sg.ProgressBar(10001, orientation='h', size=(20, 20), key='progressbar')],
              []]

    return sg.Window('Custom Progress Meter').Layout(layout)


