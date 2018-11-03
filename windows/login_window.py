# -*- coding:utf-8 -*-
import PySimpleGUI as sg


def create_login_window(msg):
    welcome_text = sg.Text(msg)
    user_text = sg.Text('UserName', size=(10, 1))
    password_text = sg.Text('Password', size=(10, 1))
    user_input = sg.InputText(size=(20, 1), key='user')
    password_input = sg.InputText(password_char='*', size=(20, 1), key='password')
    login_button = sg.Button('Login')
    layout = [
        [welcome_text],
        [user_text, user_input],
        [password_text, password_input],
        [login_button]
              ]
    return sg.Window('User Login').Layout(layout)

