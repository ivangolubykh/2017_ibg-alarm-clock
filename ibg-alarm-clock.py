#!/usr/bin/python3
import base64
import io
from tkinter import *
from locale import getdefaultlocale
from sys import platform
__author__ = 'Иван Голубых'
__site__ = 'https://github.com/ivangolubykh/2017_ibg-alarm-clock'
try:
    from PIL import Image  # pip3 install Pillow
    from pystray import Menu, MenuItem  # pip3 install pystray
# except ModuleNotFoundError:
except ImportError:
    error_text = '''Please install PIL and systray:
        pip3 install Pillow
        pip3 install pystray'''
    print(error_text)

    try:
        root = Tk()
        root.title('IBG-Alarm-Clock')
        vidj_error_text = Label(root, text=error_text)
        vidj_error_text.place(x=5, y=5)
        root.mainloop()
    except Exception as a:
        print('Please run the program from GUI-interface')

    sys.exit()


class Texts:
    ''' Выбор языка текстов программы
    '''
    @staticmethod
    def get(config=None):
        ru_text = {'porgam_name': 'Будильник ИБГ',
                   'about': 'О программе',
                   }
        en_text = {'porgam_name': 'IBG-Alarm-Clock',
                   'about': 'About',
                   }
        if config:
            language = config['language']
        else:
            language = getdefaultlocale()[0]
        if language == 'ru_RU':
            return ru_text
        return en_text


def main():
    texts = Texts.get()


if __name__ == '__main__':
    try:
        root = Tk()
        del root
    except Exception as a:
        print('Please run the program from GUI-interface')
        sys.exit()
    main()
