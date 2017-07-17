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
        qApp, QSystemTrayIcon, QMenu  # pip3 install PyQt5
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


class GlobVar:
    reload = False


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
    _IMG_TO_TRAY_24X24_BASE64 = '''R0lGODlhGAAYAOf/AAAkhQAphwAtjQAsogAtmwAtowA
    tpAA0kwAzoAswpwA1mwA2lQA3nQE4mBQznAY5oQw7lQA+nBs1pgA/nw07ow48nABApgBBoQBBq
    BQ9nwJCqQBEqQlEpBpAogpEqwBJrwBKqRFGpxFGrQBLsgBMswBNshZIsARNtABPtABRsChFtgB
    RtxtJuAxPtipGtx1LrABTuB5KuQBUuQBUuhBQtyBLuwBVvABWtQBWvRNRuABXvgBYtzBKtQBYv
    TFLtgRYvwBZxBlTughZuQBbwABcuilQuQlZwABdwh5WsQBdygBftwBewyxTsCBXsgBeyy1UsQB
    gvxFbwgBhuQBgxQBgxgBhwBRcvQBhyDBWsxhdxANjyidbtgBoxipduApk0g5lzCFjty9fuxJmz
    QBt2i9krABu1DRivwBv2htp0AZv1ipnwgBx3TpmokpfwAxw1wBz3zRpqy1pxAB04AB14QB24gB
    45SdwyzRtyQB65xt21gV76C1zzgx86U5txjJ20QCC9gCD8ACD9xV+6wCG5ACE+DV41ACF+Sl91
    zV7yQCH+QCI+h2C4i1/2R+B7yGF3w6L6gCO+jSD3ld+qlmArFqBrV2EsWOB1mCHtGuD0jmR7G6
    F1WWLuHGI2HWJzGGRvHmJ1HqK1WyTwHWO2HyM2HaP2W6VwneQ2niR23+P22qXynmS3GyYy1Sd7
    YCT13eYwIKS3YGU2YOT3oKV2nSbyISU4IOW24aW4oWY3YqY14aZ3n6fx4ib4Imc4Yue45Kf35O
    g4JSh4Yan0JCi6JWi4paj5JKl6pil5p6m4Zqn55uo6Zyp6qqsqZ2q66utqqOr55+s7a6wrZ+v6
    aau6qCw6rWwr7axsLGzr6Ky7Kmy7bS2s7q1tLW3tLe5tqy37L64t7i6t6247bq8ucG8ury+u77
    BvcLEwbXF8sTGw77F9cfJxsHJ+MrMycfK9NHNvsjL9cnM98rN+NHRyM/O89DP9NHT0NHQ9dLR9
    trV09va0eTj2uri2uno3+7t5PT38/7//P///yH5BAEKAP8ALAAAAAAYABgAAAj+AP/9y+MoEqN
    DhfzssXMnjhozYbpswYLlRQeB/1iZs1ev3rx58uTBe/fOnUl36lKiy4Xl36Bu4LBduyZtWjRnz
    5QpS4YMmbFixIQJY4bpX6Zjw4YB++WrFy9eu3blynXLFi1asbKiGgXhEa5bVGvVkgULlqpTpki
    REgXq0ydOnDRZqrCoUxsfePPW4FGjBou/LlyoGFykzwU3EgYUWMy4sWPGAxJUyEIAgeXLmDNnd
    lAhigIGoEOLHj2awoUfFFKrXs26tYUNQTBomE27tm3bHkLQ+MC7t+/fwEt8aHGiuPHjyJPTQFF
    CBoznMGRIn05dOvToKEwY2f5DiJAdO5rUILmBpHz5JkO2G4kCQ8SU90CC6bu3rpw4btuyafs2r
    h2ZI+9NAYMHYnzxhRO6eANNM8ss0ww025CTDj37sDGFgWLIUEIZaKDhhSvUWFNNNuGcEw8++fD
    Tjz9wfNFhGUfI8MYZZ4yByCSSUFLJJZt4Ekopq6wyCxg0nvHGEUnQoSQdcrjh5JNQOvnGknW8J
    wgfWGap5ZZbNiIFDHoEIuaYZJZZJiAC9VCHIYYQ4qabbCYiJ5t0JgKJEhj9w0EECwgAQAACHNB
    ABByAkMINREDBBRQYBQQAOw=='''

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
        self._create_tray_icon()
        self.setGeometry(120, 150, 300, 150)
        self.setWindowTitle(self.texts['porgam_name'])
        self.show()

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
        self.toolbar = self.addToolBar('main_toolbar')
        self.toolbar.addAction(self.methods['to_tray_action'])
        self.toolbar.addAction(self.methods['exit_action'])

    def _create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(QPixmap.fromImage(
            self._base64_to_qimge(self._IMG_CLOCK_48X48_BASE64, 'GIF'))))

        # Меню у иконки в трее:
        show_action = QAction(self.texts['tray_menu_show'], self)
        hide_action = QAction(self.texts['tray_menu_hide'], self)
        quit_action = QAction(self.texts['tray_menu_exit'], self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self._quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

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

    def _get_config(self):
        if 'win' in sys.platform:
            try:
                reestr = winreg.QueryValue(winreg.HKEY_CURRENT_USER,
                                           'Software\\' + self.config_name)
            except Exception:
                reestr = '{}'
            self.config = json.loads(reestr)
        else:
            os.chdir(os.path.expanduser('~'))
            file_path = os.path.join('.config/ibg-alarm-clock',
                                     self.config_name)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.config = json.loads(file.read())
            else:
                self.config = {}

    def _get_menu_method(self):
        self.methods = {}

        def _generate_method(self=None, method_name=None, img=None,
                             img_type=None, menu_text=None,
                             statusbar_text=None, triggered=None):
            if self is None or method_name is None or menu_text is None\
               or statusbar_text is None or triggered is None:
                return None
            if img is None or img_type is None:
                methods = QAction(menu_text, self)
            else:
                methods = QAction(
                    QIcon(QPixmap.fromImage(self.
                                            _base64_to_qimge(img, img_type))),
                    menu_text, self)
            methods.setStatusTip(statusbar_text)
            methods.triggered.connect(triggered)
            return methods

        self.methods['exit_action'] = _generate_method(
            self=self, method_name='exit_action',
            img=self._IMG_EXIT_24X24_BASE64,
            img_type='GIF',
            menu_text=self.texts['menu_exit'],
            statusbar_text=self.texts['menu_exit_statusbar'],
            triggered=self._quit,
            )

        self.methods['lang_setting_action_en'] = _generate_method(
            self=self, method_name='lang_setting_action_en',
            img=None,
            img_type=None,
            menu_text=self.texts['menu_setting_lang_en'],
            statusbar_text=self.texts['menu_setting_lang_en_statusbar'],
            triggered=self._set_language_en,
            )
        lang_status = True if self.config['language'] == 'en_EN' else False
        self.methods['lang_setting_action_en'].setCheckable(True)
        self.methods['lang_setting_action_en'].setChecked(lang_status)

        self.methods['lang_setting_action_ru'] = _generate_method(
            self=self, method_name='lang_setting_action_ru',
            img=None,
            img_type=None,
            menu_text=self.texts['menu_setting_lang_ru'],
            statusbar_text=self.texts['menu_setting_lang_ru_statusbar'],
            triggered=self._set_language_ru,
            )
        lang_status = True if self.config['language'] == 'ru_RU' else False
        self.methods['lang_setting_action_ru'].setCheckable(True)
        self.methods['lang_setting_action_ru'].setChecked(lang_status)

        self.methods['reset_setting_action'] = _generate_method(
            self=self, method_name='reset_setting_action',
            img=self._IMG_RESET_24X24_BASE64,
            img_type='GIF',
            menu_text=self.texts['menu_setting_reset'],
            statusbar_text=self.texts['menu_setting_reset_statusbar'],
            triggered=self._reset_settings,
            )

        self.methods['to_tray_action'] = _generate_method(
            self=self, method_name='to_tray_action',
            img=self._IMG_TO_TRAY_24X24_BASE64,
            img_type='GIF',
            menu_text=self.texts['menu_to_tray'],
            statusbar_text=self.texts['menu_to_tray_statusbar'],
            triggered=self._minimize_to_tray,
            )

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
                   'tray_menu_show': 'Развернуть окно',
                   'tray_menu_hide': 'Свернуть окно',
                   'tray_menu_exit': 'Выход',
                   'tray_minimized_message': 'Приложение свёрнуто в'
                                             ' системный трей',
                   'menu_to_tray': 'Свернуть окно в трей',
                   'menu_to_tray_statusbar': 'Свернуть окно в трей',
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
                   'tray_menu_show': 'Show',
                   'tray_menu_hide': 'Hide',
                   'tray_menu_exit': 'Exit',
                   'tray_minimized_message': 'Application was minimized'
                                             ' to Tray',
                   'menu_to_tray': 'Minimize the window to the tray',
                   'menu_to_tray_statusbar': 'Minimize the window to the tray',
                   }
        if not hasattr(self, 'config'):
            self.config = {}
        if 'language' not in self.config:
            self.config['language'] = getdefaultlocale()[0]
        if self.config['language'] == 'ru_RU':
            self.texts = ru_text
        else:
            self.texts = en_text

    def _minimize_to_tray(self):
        self.hide()
        self.tray_icon.showMessage(
            self.texts['porgam_name'],
            self.texts['tray_minimized_message'],
            QIcon(QPixmap.fromImage(
                self._base64_to_qimge(self._IMG_CLOCK_48X48_BASE64, 'GIF'))),
            2000
        )

    def _reload(self):
        GlobVar.reload = True
        self._quit()

    def _reset_settings(self):
        self._del_config()
        self.config = {}
        self._reload()

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

    def _set_language(self, lang):
        self.config['language'] = lang
        self._save_config()
        self._reload()

    def _set_language_en(self, lang):
        self._set_language('en_EN')

    def _set_language_ru(self, lang):
        self._set_language('ru_RU')

    def _quit(self):
        self._save_config()
        qApp.quit()

    def closeEvent(self, event):
        '''Переопределение метода closeEvent, для перехвата события закрытия
         окна. Окно будет сворачиваться в системный трей'''
        event.ignore()
        self._minimize_to_tray()


@is_gui
def main():
    if 'win' not in sys.platform and sys.platform != 'linux':
        # Поддерживается только Windows и Linux
        print('The operating system is not defined.'
              ' Supported OS: Windows, Linux.')
        sys.exit()

    GlobVar.reload = True
    while GlobVar.reload:
        GlobVar.reload = False
        app = QApplication(sys.argv)
        clock = AlarmClock()
        # sys.exit(app.exec_())
        app.exec_()
        del clock
        del app


if __name__ == '__main__':
    main()
