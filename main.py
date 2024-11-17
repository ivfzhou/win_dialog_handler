# Copyright (c) 2024 ivfzhou
# win_dialog_handler is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import json
import os
import sys
import time

import clipboard
from pywinauto import base_wrapper
from pywinauto import findwindows
from pywinauto.controls import hwndwrapper
from pywinauto.controls import win32_controls
from uiautomation import DocumentControl


class Rsp:
    result = False
    message = ''
    data = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def handle(f):
    while True:
        time.sleep(3)
        try:
            with open(f, 'r+', encoding='utf-8') as file:
                content = file.read().strip()
                lines = content.split('\n')
                lines.reverse()
                line = ''
                for line in lines:
                    if line != '':
                        break
                if line == '':
                    file.close()
                    continue
                if line.startswith('ask: '):
                    rsp = ''
                    data = json.loads(line[4:])
                    method = data['method']
                    if method == 'get_dialog':
                        rsp = get_dialog(data['title']).to_json()
                    elif method == 'click_button':
                        rsp = click_button(data['title'], data['but'], data['index']).to_json()
                    elif method == 'list_window':
                        rsp = list_window().to_json()
                    elif method == 'close_windows':
                        rsp = close_windows(data['title'], data['index']).to_json()
                    elif method == 'get_cmd_content':
                        rsp = get_cmd_content(data['index']).to_json()
                    elif method == 'send_cmd_content':
                        rsp = send_cmd_content(data['content'], data['index']).to_json()
                    else:
                        print('no title match ' + method)
                    if rsp != '':
                        file.seek(0, 2)
                        file.write('\nanswer: ')
                        file.write(rsp)
                file.close()
        except BaseException as e:
            print(str(e))


def get_dialog(title):
    print('get dialog ' + title)
    res = Rsp()
    res.data = {"titles": [], "content": []}
    try:
        for v in findwindows.find_windows():
            hw = hwndwrapper.HwndWrapper(v)
            curTitle = str(hw.window_text())
            res.data["titles"].append(curTitle)
            if curTitle == title:
                res.result = True
                curContent = ''
                children = hw.children()
                for child in children:
                    curContent += str(base_wrapper.BaseWrapper.window_text(child))
                res.data["content"].append(curContent)
    except BaseException as e:
        res.result = False
        res.data = None
        res.message = repr(e)
    return res


def click_button(title, but, index):
    print("click button " + title + " " + but)
    res = Rsp()
    res.result = False
    try:
        cur = 0
        dialogs = findwindows.find_windows()
        for v in dialogs:
            hw = hwndwrapper.HwndWrapper(v)
            curTitle = str(hw.window_text())
            if curTitle == title:
                if cur != index:
                    cur += 1
                    continue
                children = hw.children()
                for child in children:
                    text = str(base_wrapper.BaseWrapper.window_text(child))
                    if text.__contains__(but):
                        win32_controls.ButtonWrapper.click(child, double=True)
                        res.result = True
                        return res
                return res
    except BaseException as e:
        res.message = repr(e)
    return res


def list_window():
    print('list window')
    res = Rsp()
    res.result = False
    try:
        res.result = True
        res.data = []
        dialogs = findwindows.find_windows()
        for v in dialogs:
            hw = hwndwrapper.HwndWrapper(v)
            res.data.append(hw.window_text())
    except BaseException as e:
        res.result = False
        res.message = repr(e)
    return res


def close_windows(title, index):
    print('close window ' + title)
    res = Rsp()
    res.result = False
    try:
        cur = 0
        dialogs = findwindows.find_windows()
        for v in dialogs:
            hw = hwndwrapper.HwndWrapper(v)
            curTitle = str(hw.window_text())
            if curTitle == title:
                if cur != index:
                    cur += 1
                    continue
                hw.close()
                res.result = True
                return res
    except BaseException as e:
        res.message = repr(e)
    return res


def get_cmd_content(index):
    print('get cmd content')
    res = Rsp()
    res.result = False
    try:
        window = DocumentControl(Name="Text Area", searchDepth=3, foundIndex=index)
        if window.Exists():
            res.result = True
            window.SendKeys('{Ctrl}A')
            window.SendKeys('{Ctrl}C')
            data = clipboard.paste()
            res.data = str(data)
            res.data = res.data.replace('\n', r'\n')
    except BaseException as e:
        res.message = repr(e)
    return res


def send_cmd_content(content, index):
    print('send cmd content ' + content)
    res = Rsp()
    res.result = False
    try:
        window = DocumentControl(Name="Text Area", searchDepth=3, foundIndex=index)
        if window.Exists():
            res.result = True
            window.SendKeys(content)
    except BaseException as e:
        res.message = repr(e)
    return res


def main():
    username = os.getlogin()
    print('run win_dialog_handler in ' + username)
    handle(sys.argv[1])


main()
