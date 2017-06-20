#!/usr/bin/python3
import base64
import json
import sys
import os
from tkinter import Tk, Label
from locale import getdefaultlocale
__author__ = 'Иван Голубых'
__site__ = 'https://github.com/ivangolubykh/2017_ibg-alarm-clock'
if 'win' in sys.platform:
    import winreg


def is_gui():
    try:
        root = Tk()
        root.destroy()
        del root
    except Exception as a:
        print('Please run the program from GUI-interface')
        sys.exit()
    return True


try:
    from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton,\
        QApplication  # pip3 install PyQt5
    from PyQt5.QtGui import QImage, QIcon, QPixmap
    from PyQt5.QtCore import QByteArray
except ImportError:
    error_text = '''Please install PyQt5:
        pip3 install PyQt5'''
    print(error_text)
    if is_gui():
        root = Tk()
        root.title('IBG-Alarm-Clock')
        vidj_error_text = Label(root, text=error_text)
        vidj_error_text.place(x=5, y=5)
        root.mainloop()


class AlarmClock(QWidget):
    _IMG_CLOCK_48X48_BASE64 = '''R0lGODlhMAAwAOf/AAASrgATrwAUsAAWqQAXqgkXtAAas
    QAbswAcqwActAAerQAetgAgrwAhsQAiqgAisgMjswgktAwlrQwltQAqpwAptgAqrgAqrwAqtwA
    rsQAtpAAtswAurBcqowwvthAxsAA3rBIyqRMysRg0pQc5thw0tB02pws6tw46sSA2tiA3sBM7u
    RQ8syM5qxY8uhg+rQtEuR0/tyJBuSNCsxNGvDFBrjFDqChFtipFvi1HuTFLthVP4jJMsTNNsjN
    OrCxRvDhPvC5SvTlSsSRU4SZU8BRZ9DxVtCpW6z9VvB1b7y1X7TtU7DFZ7iNd8URZwENaukJbt
    DRa8CZe8jZb8UVcvDZc6yhg7Tdd5Tdc80ZdvTle5kdfuDle7UhguT1i40xjvUZlxEFj7E5lv0F
    l5k1muVBkxVNlszho70Vo41JqvllpuElp7FBvyVZuwkxu41lwxFtyxmBzu1F04Vh01VRz71xz4
    l12xFV08F132WZ4wWJ65Gh9v2B92Gl+wGh91HF/vWyAw25/yW+Aym6CxWaC3nCEx3aIv3WJzHu
    JyHmJ1ICJwm+M4nyNxH+QyH+P24CRyX6R1YWSxIOUzH6U5YWWzo6Vw4eY0ImX1oyYy4ma05Cfy
    5Ke0Yqg3pSg046g5pigzpqlzJam0pqm2pmp1aCr0p6u26uuy6ev0KGw3aOv462wzauzyKuy1Ki
    z2661yq+22LK20qi45bG4za651LG42rS41K654ba51au76K+74ra+07bB3LfC3b7F27/G3MHF4
    rvH4r/G6cDH3b7J5cDL5sXN4srO3cvP7MbR7cnR5s3R7sfT7srW8dPX59HZ79TZ6dLa8Nbb3dP
    b8dTc8t3e6Nvg497f6eHf49/g6uPh5eLi7eTl7+nm6+bo5ebn8evo7eXq7ebq++nq9O3s4+zs9
    +/s8evu6u3t+Orv8u/v5fHw5vPx9e7z9vHz8PTy9u/19/b0+PL3+vb49fX6/fj69/z5/vb7/vn
    7+Pf9//v9+vj+///+9fz/+///9v7//P///yH5BAEKAP8ALAAAAAAwADAAAAj+AP0JHEhQoCYLE
    RIqXMiwYYQQwwpKnDgQXgqHGDOWocixoB0DCQ2IHEmy5MiEBEZ1XCmwVQQa0dLJnEmzpjpfIiy
    AY8kSVwRiPAsOsiAuaEdeP40ODOThnFKKyyLYeurvTQl3VCVya0CJ6hMX97JKZEDG3zE8c9KqX
    ZuWkDZ/MnqIlQiFgr8wXPLq3at3SiJ/BB7NLVgrQDU/U/gq5hIl1SkA3QYTtGehkLEji/kSaWd
    jhuSCSGD4Q5N5Lx9xFTJ9JigMQDFPiUtzYRaJwc7VA7dYGIc5sxQv5gg0wk0QWwRLsaJkPtKMC
    ot8xAlqGlDMjRTFUyaRQlAsesE8G6j+DVF8RVeEV94lskGBqsheLa4kYEo/0YmOStfzkqrAiD7
    FNjmMssMQu3AAin8c9SDKPv58kQeCHNXTgT/ymAAhR/rcYI0ph1xIkT4ybDOLIB5OhI6F/mhQY
    kHsqECLQHk8saJA9gDxBUEv/LGiPThsUdA6IsTh4T1GBAFdQeVw0MeFYpAAD0XPRPAJgoZI8E1
    HvSAwC33NRKDSSmmUQE96PqC40j4I7OHdLQY8E1QnDLxF3A854DNQPOEk44oszpATlkDeVCAJc
    fZIgMhAl5zBWBRRSGHFGlMJ5EMLxLESQDb+fCOHcostsYg9/sACwDW4GcGBQHXIlhckAiGgyGq
    F+zCghj+c9CbbEcHApcNq2zSAiTyq7qWHP1SsMM9nyESQyzTB6jUGPnBc9RlSxCiTX7P1CNLUZ
    z798g4edNwh7rjkikuHI/4AQtRnoUTAAjDQSCPvvPTWq4oFFkQjmRkBRDCBSQCTdABKm8wVDwk
    ZJcwQGIOVggIIEEcs8cQUg1BDMh0FBAA7'''

    def __init__(self, config_name=''):
        super().__init__()
        self.config_name = 'ibg-alarm-clock_' + str(config_name) + '.cfg'
        self._get_config()
        self._get_text()
        self.setGeometry(120, 150, 300, 150)
        self.setWindowTitle(self.texts['porgam_name'])

        self._icon_bytes64 = base64.b64decode(__class__.
                                              _IMG_CLOCK_48X48_BASE64.
                                              encode())
        self._icon_bytes = QByteArray(self._icon_bytes64)
        self._icon_image = QImage.fromData(self._icon_bytes, "GIF")
        self.setWindowIcon(QIcon(QPixmap.fromImage(self._icon_image)))

    def _get_text(self):
        ''' Выбор языка текстов программы
        '''
        ru_text = {'porgam_name': 'Будильник ИБГ',
                   'about': 'О программе',
                   'exit': 'Выход',
                   'open_window': 'Показать будильники',
                   }
        en_text = {'porgam_name': 'IBG-Alarm-Clock',
                   'about': 'About',
                   'exit': 'Exit',
                   'open_window': 'Show alarm clocks',
                   }
        # if self.config:
        if False:
            language = self.config['language']
        else:
            language = getdefaultlocale()[0]
            self.config['language'] = language
        if language == 'ru_RU':
            self.texts = ru_text
        else:
            self.texts = en_text

    def _get_config(self):
        if 'win' in sys.platform:
            reestr = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                      'Software\\' + self.config_name)
            self.config = json.loads(winreg.QueryValue(reestr, None))
        else:
            os.chdir(os.path.expanduser('~'))
            file_path = os.path.join('.config/ibg-alarm-clock',
                                     self.config_name)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.config = json.loads(file.read())
            else:
                self.config = {}

    def _save_config(self):
        json_config = json.dumps(self.config)
        if 'win' in sys.platform:
            reestr = winreg.SetValue(winreg.HKEY_CURRENT_USER,
                                     'Software\\' + self.config_name,
                                     winreg.REG_SZ,
                                     json_config)
        else:
            os.chdir(os.path.expanduser('~'))
            file_path = '.config/ibg-alarm-clock'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            os.chdir(file_path)
            with open(self.config_name, 'w', encoding='utf-8') as file:
                file.write(json_config)

    def _del_config(self):
        if 'win' in sys.platform:
            reestr = winreg.DeleteKey(winreg.HKEY_CURRENT_USER,
                                      'Software\\' + self.config_name)
        else:
            os.chdir(os.path.expanduser('~'))
            file_path = '.config/ibg-alarm-clock'
            if os.path.exists(os.path.join(file_path, self.config_name)):
                os.remove(os.path.join(file_path, self.config_name))
                os.chdir(os.path.expanduser('~'))
                os.removedirs(file_path)


def main():
    is_gui()

    if 'win' not in sys.platform and sys.platform != 'linux':
        # Поддерживается только Windows и Linux
        print('The operating system is not defined.'
              ' Supported OS: Windows, Linux.')
        sys.exit()

    app = QApplication(sys.argv)
    clock = AlarmClock()
    clock.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
