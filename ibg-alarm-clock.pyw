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


def is_gui(function_to_decorate):
    def wrapper(*args, **kwargs):
        function_to_decorate(*args, **kwargs)

    try:
        root = Tk()
        root.destroy()
        del root
    except Exception as a:
        print('Please run the program from GUI-interface')
        sys.exit()
    else:
        return wrapper


try:
    from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, \
        qApp  # pip3 install PyQt5
    from PyQt5.QtGui import QImage, QIcon, QPixmap
    from PyQt5.QtCore import QByteArray
except ImportError:
    error_text = " Please install PyQt5:\npip3 install PyQt5"
    print(error_text)

    @is_gui
    def gui_help_install():
        root = Tk()
        root.title('IBG-Alarm-Clock')
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.wm_geometry("+%d+%d" % (x, y))  # По центру экрана
        vidj_error_text = Label(root, text=error_text)
        vidj_error_text.place(x=5, y=5)
        root.mainloop()

    gui_help_install()
    sys.exit()


class AlarmClock(QMainWindow):
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
    _IMG_EXIT_24X24_BASE64 = '''R0lGODlhGAAYAMZqAAGsKAKsKQOsKgStKwWtLAatLQeuLQ
    iuLgmuLwqvMAuvMQ+wNBGxNhKxNxOyOBSyOBazOhezOxizPBm0PRq0PR21QB+2QiC2QiG2QyK3
    RCe4SCy6TS26TTO8UzS8UzW9VDa9VTe9Vjm+WDu/WT2/Wz7AXETCYUbCY0nDZUvEZ0zEaE3FaE
    /FalDGa1THblzJdV3Kdl/KeGHLeWLLemTMfGnOgHDQhnbSi3rTjnvUj4LWlYPWlobXmIrYnI7a
    n5Lbo5fdp5veqp7fraHgr6LgsKXhs6rjt63kua7kuq/ku7PmvrTmv7jnw7zpxr3px8DqycHqys
    PrzMjt0Mrt0svu08zu1M3u1NTx2tbx3Nny3try39zz4d704+L15uf36ur47fH68/P79Pb89/f8
    +Pn9+fr9+vv9+/z+/P3+/f7+/v////////////////////////////////////////////////
    ///////////////////////////////////////yH5BAEKAH8ALAAAAAAYABgAQAf+gACCggMH
    BocGBwmJCIcHAYORABNqHwBbajySAEpqLZsANR4RERSCJWpkJQAbY2pqK6CTZK+1ryODRrCyE7
    RqaZFRtrugF2XDtl9LTGcmvL61TVRaghZixJu9akgHAwMGBQYEMmevsaAVVUVmaj+RV2ousoMQ
    0AAWYA4AOrbnkRocTiCrdUTQEmyRqJQRw7ChGDJZBDnJMQ8AgydTMk6pQoSGFCpFrky5QuLZMC
    BpQAwKgjCSNjVbqFSpYiWJiBRDzD3DsoDCDhyShOgEhcEdSy8WBoXoAUBAjAcmfzUYNONXLRZR
    gQEgAADFMH+RArSodQVABjU+ACiAUgusoBszLzpsmMtBRZdXYQTZGLpJArRhaGAAiFDGLSElaQ
    aq4XIBgJAboAxEaEC5MmV9AAxAABUIADs='''
    _IMG_RESET_24X24_BASE64 = '''R0lGODlhGAAYAOfDAEoQEWUREVgVFVsVFV8XF18XGGMXF
    3EXF3IXF2sZGXQXF3EYGHIYGHEZGW0dHW4dHXQdHXMeHm8gHXceHncfH3sfH3wfH4YeHokfH4Q
    hIYkhIYQkJIkkJHkpKYonJwxPFpEnJ5AoKJkmJqElJRBTFpcpKYoxMZ8sLBVXGRZYG6QtLRRaG
    xBcGJQzMxdcHBlcHRNfGbIuLpk4OBZiHBphHhVjGxliHhdkHKk2NhZlHBplIBhnGxhnHBhnHas
    5ORtnH7E8PMk3NxxtHxpuHRtwIR5zIx50Ix11Hx11Ih12JCV1KcVDQx96I8JHRyV6KSt7LrxNT
    SSCJtlJSSeCKiKFJNlMTCeGKeBMTCGKJCeIKMtTU9pQUN5RUdtTU91TU9FYWNpXV8NfX99aWjO
    RNTqQPN9cXDCVMt1fXzOXM+BgYOFgYOVgYOJhYSujJt9nZ+JpadtsbCmpJkubTuVra+Ntbedsb
    OFvb+VubuRvb0iiSORwcDypN+V1deZ4eEqtSDe2Lzy1NUmwRed9fe58fOd+fumAgOiBgUO7Oz+
    9NuyCguuDg+mEhEO9PES+PEW+PeqIiOqKilm7Vle9U07BRk/CR+uPj1LESlTETe+QkFfEUFLHS
    ljFUlbGTuyTk2nDZVzJU17JV+2ZmXTCc+6ammDLWWfNYGjOYW3OaGvPZGzQZWrRY23QZm3RZfG
    kpHjVcnfXb3zXdXrYdH7Zd3/ZeH/Zen3cdYTcfoPdfIjcg4jdgYXffo7giJDhipPijZblj5jlk
    qDpmqnxpLHyq//////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////
    //////////////////////////////////yH5BAEKAP8ALAAAAAAYABgAQAj+AP8JHEiwoMGDG
    xR1amXCIIk9jgDxODgQwEEluHbZykNxII46dO6cAXJCxIgLEDpW6JLmDR49dLQUWNEjRw0yvnL
    F8gNjxo0UHQUyiWJlipGgBjOEKAGCA9KCPgo9wuTh4AeDBBgcWABFEKRKLRAoaFCAhSRWqUyBs
    nRoiEELVbgsGWBQjrBftGwg/ZEEC5UsaDaVQqVqzNPDiBMfVAGmjBgvUoJgQBzBTR9BcCYYfOC
    gYwA7kEaFOYiizY6OMhZ1CtWhoItAnzhRaiSEoIYra+bwIWQo0aAvEnREqnVrlqtVpDQhOkKQw
    pYyatg0MVDwSbBeupx0TBBDwEFRwHgeeXrRkQYNg0ROyYL1qghiJHH+MJp0KZMZxfjzEwwIADs
    ='''

    def __init__(self, config_name=''):
        super().__init__()
        self.config_name = 'ibg-alarm-clock_' + str(config_name) + '.cfg'
        self._get_config()
        self._get_text()
        self._create_icon_windows()
        self.statusBar()
        self._get_menu_method()
        self._create_menu()
        self._create_toolbar()
        self.setGeometry(120, 150, 300, 150)
        self.setWindowTitle(self.texts['porgam_name'])
        self.show()

    def _get_text(self):
        ''' Выбор языка текстов программы
        '''
        ru_text = {'porgam_name': 'Будильник ИБГ',
                   'about': 'О программе',
                   'exit': 'Выход',
                   'open_window': 'Показать будильники',
                   'menu_file': 'Файл',
                   'menu_exit': 'Выход',
                   'menu_exit_statusbar': 'Выход из программы',
                   'menu_setting': 'Настройки',
                   'menu_setting_lang': 'Язык программы (Language)',
                   'menu_setting_lang_en': 'Английский (English)',
                   'menu_setting_lang_en_statusbar':
                       'Установить английский язык (English language)',
                   'menu_setting_lang_ru': 'Русский (Russian)',
                   'menu_setting_lang_ru_statusbar':
                       'Установить русский язык (Russian language)',
                   'menu_setting_reset': 'Сброс настроек',
                   'menu_setting_reset_statusbar': 'Сбросить настройки'
                                                   ' программы',
                   }
        en_text = {'porgam_name': 'IBG-Alarm-Clock',
                   'about': 'About',
                   'exit': 'Exit',
                   'open_window': 'Show alarm clocks',
                   'menu_file': 'File',
                   'menu_exit': 'Exit',
                   'menu_exit_statusbar': 'Exit application',
                   'menu_setting': 'Settings',
                   'menu_setting_lang': 'Language',
                   'menu_setting_lang_en': 'English',
                   'menu_setting_lang_en_statusbar': 'Set English language',
                   'menu_setting_lang_ru': 'Russian (Русский)',
                   'menu_setting_lang_ru_statusbar': 'Set Russian language',
                   'menu_setting_lang_statusbar': 'Change the language'
                                                  ' of the program',
                   'menu_setting_reset': 'Reset',
                   'menu_setting_reset_statusbar': 'Reset program settings',
                   }
        if not hasattr(self, 'config'):
            self.config = {}
        if 'language' not in self.config:
            self.config['language'] = getdefaultlocale()[0]
        if self.config['language'] == 'ru_RU':
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

    @staticmethod
    def _base64_to_qimge(base64_text, format='GIF'):
        icon_bytes64 = base64.b64decode(base64_text.encode())
        icon_bytes = QByteArray(icon_bytes64)
        return QImage.fromData(icon_bytes, format)

    def _create_icon_windows(self):
        '''Создание иконки в верхнем левом углу окна в ОС Windows, а так же
        иконки панели задач для Linux'''
        self.setWindowIcon(
            QIcon(QPixmap.fromImage(
                self.__class__._base64_to_qimge(self._IMG_CLOCK_48X48_BASE64,
                                                'GIF'))))

    def _get_menu_method(self, a=True):
        self.methods = {}
        # methods['exit_action'] = QAction(QIcon('exit.png'), '&Exit', self)
        self.methods['exit_action'] = \
            QAction(
                QIcon(
                    QPixmap.fromImage(
                        self._base64_to_qimge(self._IMG_EXIT_24X24_BASE64,
                                              'GIF'))),
                self.texts['menu_exit'], self)
        self.methods['exit_action'].\
            setStatusTip(self.texts['menu_exit_statusbar'])
        self.methods['exit_action'].triggered.connect(qApp.quit)

        self.methods['lang_setting_action_en'] = \
            QAction(self.texts['menu_setting_lang_en'], self)
        self.methods['lang_setting_action_en'].\
            setStatusTip(self.texts['menu_setting_lang_en_statusbar'])
        self.methods['lang_setting_action_en'].triggered.\
            connect(self._set_language_en)
        lang_status = True if self.config['language'] == 'en_EN' else False
        self.methods['lang_setting_action_en'].setCheckable(True)
        self.methods['lang_setting_action_en'].setChecked(lang_status)

        self.methods['lang_setting_action_ru'] = \
            QAction(self.texts['menu_setting_lang_ru'], self)
        self.methods['lang_setting_action_ru'].\
            setStatusTip(self.texts['menu_setting_lang_ru_statusbar'])
        self.methods['lang_setting_action_ru'].triggered.\
            connect(self._set_language_ru)
        lang_status = True if self.config['language'] == 'ru_RU' else False
        self.methods['lang_setting_action_ru'].setCheckable(True)
        self.methods['lang_setting_action_ru'].setChecked(lang_status)

        self.methods['reset_setting_action'] = \
            QAction(
                QIcon(
                    QPixmap.fromImage(
                        self._base64_to_qimge(self._IMG_RESET_24X24_BASE64,
                                              'GIF'))),
                self.texts['menu_setting_reset'], self)
        self.methods['reset_setting_action'].\
            setStatusTip(self.texts['menu_setting_reset_statusbar'])
        self.methods['reset_setting_action'].\
            triggered.connect(self._reset_settings)

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu(self.texts['menu_file'])
        file_menu.addAction(self.methods['exit_action'])

        setting_menu = menubar.addMenu(self.texts['menu_setting'])
        lng_settings_menu = setting_menu.addMenu(self.
                                                 texts['menu_setting_lang'])
        lng_settings_menu.addAction(self.methods['lang_setting_action_en'])
        lng_settings_menu.addAction(self.methods['lang_setting_action_ru'])
        setting_menu.addAction(self.methods['reset_setting_action'])

    def _create_toolbar(self):
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.methods['exit_action'])

    def _set_language(self, lang):
        self.config['language'] = lang
        self._save_config()
        self.__init__()
        # self.methods['lang_setting_action_ru'].setChecked(lang)

    def _set_language_ru(self, lang):
        self._set_language('ru_RU')

    def _set_language_en(self, lang):
        self._set_language('en_EN')

    def _reset_settings(self):
        self._del_config()
        self.__init__()


@is_gui
def main():
    if 'win' not in sys.platform and sys.platform != 'linux':
        # Поддерживается только Windows и Linux
        print('The operating system is not defined.'
              ' Supported OS: Windows, Linux.')
        sys.exit()

    app = QApplication(sys.argv)
    clock = AlarmClock()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
