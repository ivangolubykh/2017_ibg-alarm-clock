#!/usr/bin/python3
import base64
import io
from tkinter import *
from locale import getdefaultlocale
import sys
__author__ = 'Иван Голубых'
__site__ = 'https://github.com/ivangolubykh/2017_ibg-alarm-clock'
try:
    from PIL import Image  # pip3 install Pillow
    import pystray  # pip3 install pystray
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


class AlarmClock:
    _IMG_CLOCK_14_22_BASE64 = '''/9j/4AAQSkZJRgABAQEASABIAAD/4gxYSUNDX1BST0ZJT
    EUAAQEAAAxITGlubwIQAABtbnRyUkdCIFhZWiAHzgACAAkABgAxAABhY3NwTVNGVAAAAABJRUM
    gc1JHQgAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLUhQICAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABFjcHJ0AAABUAAAADNkZXNjAAABhAAAAGx3dHB0AAA
    B8AAAABRia3B0AAACBAAAABRyWFlaAAACGAAAABRnWFlaAAACLAAAABRiWFlaAAACQAAAABRkb
    W5kAAACVAAAAHBkbWRkAAACxAAAAIh2dWVkAAADTAAAAIZ2aWV3AAAD1AAAACRsdW1pAAAD+AA
    AABRtZWFzAAAEDAAAACR0ZWNoAAAEMAAAAAxyVFJDAAAEPAAACAxnVFJDAAAEPAAACAxiVFJDA
    AAEPAAACAx0ZXh0AAAAAENvcHlyaWdodCAoYykgMTk5OCBIZXdsZXR0LVBhY2thcmQgQ29tcGF
    ueQAAZGVzYwAAAAAAAAASc1JHQiBJRUM2MTk2Ni0yLjEAAAAAAAAAAAAAABJzUkdCIElFQzYxO
    TY2LTIuMQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AWFlaIAAAAAAAAPNRAAEAAAABFsxYWVogAAAAAAAAAAAAAAAAAAAAAFhZWiAAAAAAAABvogAAO
    PUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z2Rlc2MAAAAAAAA
    AFklFQyBodHRwOi8vd3d3LmllYy5jaAAAAAAAAAAAAAAAFklFQyBodHRwOi8vd3d3LmllYy5ja
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkZXNjAAAAAAA
    AAC5JRUMgNjE5NjYtMi4xIERlZmF1bHQgUkdCIGNvbG91ciBzcGFjZSAtIHNSR0IAAAAAAAAAA
    AAAAC5JRUMgNjE5NjYtMi4xIERlZmF1bHQgUkdCIGNvbG91ciBzcGFjZSAtIHNSR0IAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAZGVzYwAAAAAAAAAsUmVmZXJlbmNlIFZpZXdpbmcgQ29uZGl0aW9uI
    GluIElFQzYxOTY2LTIuMQAAAAAAAAAAAAAALFJlZmVyZW5jZSBWaWV3aW5nIENvbmRpdGlvbiB
    pbiBJRUM2MTk2Ni0yLjEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHZpZXcAAAAAABOk/gAUX
    y4AEM8UAAPtzAAEEwsAA1yeAAAAAVhZWiAAAAAAAEwJVgBQAAAAVx/nbWVhcwAAAAAAAAABAAA
    AAAAAAAAAAAAAAAAAAAAAAo8AAAACc2lnIAAAAABDUlQgY3VydgAAAAAAAAQAAAAABQAKAA8AF
    AAZAB4AIwAoAC0AMgA3ADsAQABFAEoATwBUAFkAXgBjAGgAbQByAHcAfACBAIYAiwCQAJUAmgC
    fAKQAqQCuALIAtwC8AMEAxgDLANAA1QDbAOAA5QDrAPAA9gD7AQEBBwENARMBGQEfASUBKwEyA
    TgBPgFFAUwBUgFZAWABZwFuAXUBfAGDAYsBkgGaAaEBqQGxAbkBwQHJAdEB2QHhAekB8gH6AgM
    CDAIUAh0CJgIvAjgCQQJLAlQCXQJnAnECegKEAo4CmAKiAqwCtgLBAssC1QLgAusC9QMAAwsDF
    gMhAy0DOANDA08DWgNmA3IDfgOKA5YDogOuA7oDxwPTA+AD7AP5BAYEEwQgBC0EOwRIBFUEYwR
    xBH4EjASaBKgEtgTEBNME4QTwBP4FDQUcBSsFOgVJBVgFZwV3BYYFlgWmBbUFxQXVBeUF9gYGB
    hYGJwY3BkgGWQZqBnsGjAadBq8GwAbRBuMG9QcHBxkHKwc9B08HYQd0B4YHmQesB78H0gflB/g
    ICwgfCDIIRghaCG4IggiWCKoIvgjSCOcI+wkQCSUJOglPCWQJeQmPCaQJugnPCeUJ+woRCicKP
    QpUCmoKgQqYCq4KxQrcCvMLCwsiCzkLUQtpC4ALmAuwC8gL4Qv5DBIMKgxDDFwMdQyODKcMwAz
    ZDPMNDQ0mDUANWg10DY4NqQ3DDd4N+A4TDi4OSQ5kDn8Omw62DtIO7g8JDyUPQQ9eD3oPlg+zD
    88P7BAJECYQQxBhEH4QmxC5ENcQ9RETETERTxFtEYwRqhHJEegSBxImEkUSZBKEEqMSwxLjEwM
    TIxNDE2MTgxOkE8UT5RQGFCcUSRRqFIsUrRTOFPAVEhU0FVYVeBWbFb0V4BYDFiYWSRZsFo8Ws
    hbWFvoXHRdBF2UXiReuF9IX9xgbGEAYZRiKGK8Y1Rj6GSAZRRlrGZEZtxndGgQaKhpRGncanhr
    FGuwbFBs7G2MbihuyG9ocAhwqHFIcexyjHMwc9R0eHUcdcB2ZHcMd7B4WHkAeah6UHr4e6R8TH
    z4faR+UH78f6iAVIEEgbCCYIMQg8CEcIUghdSGhIc4h+yInIlUigiKvIt0jCiM4I2YjlCPCI/A
    kHyRNJHwkqyTaJQklOCVoJZclxyX3JicmVyaHJrcm6CcYJ0kneierJ9woDSg/KHEooijUKQYpO
    ClrKZ0p0CoCKjUqaCqbKs8rAis2K2krnSvRLAUsOSxuLKIs1y0MLUEtdi2rLeEuFi5MLoIuty7
    uLyQvWi+RL8cv/jA1MGwwpDDbMRIxSjGCMbox8jIqMmMymzLUMw0zRjN/M7gz8TQrNGU0njTYN
    RM1TTWHNcI1/TY3NnI2rjbpNyQ3YDecN9c4FDhQOIw4yDkFOUI5fzm8Ofk6Njp0OrI67zstO2s
    7qjvoPCc8ZTykPOM9Ij1hPaE94D4gPmA+oD7gPyE/YT+iP+JAI0BkQKZA50EpQWpBrEHuQjBCc
    kK1QvdDOkN9Q8BEA0RHRIpEzkUSRVVFmkXeRiJGZ0arRvBHNUd7R8BIBUhLSJFI10kdSWNJqUn
    wSjdKfUrESwxLU0uaS+JMKkxyTLpNAk1KTZNN3E4lTm5Ot08AT0lPk0/dUCdQcVC7UQZRUFGbU
    eZSMVJ8UsdTE1NfU6pT9lRCVI9U21UoVXVVwlYPVlxWqVb3V0RXklfgWC9YfVjLWRpZaVm4Wgd
    aVlqmWvVbRVuVW+VcNVyGXNZdJ114XcleGl5sXr1fD19hX7NgBWBXYKpg/GFPYaJh9WJJYpxi8
    GNDY5dj62RAZJRk6WU9ZZJl52Y9ZpJm6Gc9Z5Nn6Wg/aJZo7GlDaZpp8WpIap9q92tPa6dr/2x
    XbK9tCG1gbbluEm5rbsRvHm94b9FwK3CGcOBxOnGVcfByS3KmcwFzXXO4dBR0cHTMdSh1hXXhd
    j52m3b4d1Z3s3gReG54zHkqeYl553pGeqV7BHtje8J8IXyBfOF9QX2hfgF+Yn7CfyN/hH/lgEe
    AqIEKgWuBzYIwgpKC9INXg7qEHYSAhOOFR4Wrhg6GcobXhzuHn4gEiGmIzokziZmJ/opkisqLM
    IuWi/yMY4zKjTGNmI3/jmaOzo82j56QBpBukNaRP5GokhGSepLjk02TtpQglIqU9JVflcmWNJa
    flwqXdZfgmEyYuJkkmZCZ/JpomtWbQpuvnByciZz3nWSd0p5Anq6fHZ+Ln/qgaaDYoUehtqImo
    pajBqN2o+akVqTHpTilqaYapoum/adup+CoUqjEqTepqaocqo+rAqt1q+msXKzQrUStuK4trqG
    vFq+LsACwdbDqsWCx1rJLssKzOLOutCW0nLUTtYq2AbZ5tvC3aLfguFm40blKucK6O7q1uy67p
    7whvJu9Fb2Pvgq+hL7/v3q/9cBwwOzBZ8Hjwl/C28NYw9TEUcTOxUvFyMZGxsPHQce/yD3IvMk
    6ybnKOMq3yzbLtsw1zLXNNc21zjbOts83z7jQOdC60TzRvtI/0sHTRNPG1EnUy9VO1dHWVdbY1
    1zX4Nhk2OjZbNnx2nba+9uA3AXcit0Q3ZbeHN6i3ynfr+A24L3hROHM4lPi2+Nj4+vkc+T85YT
    mDeaW5x/nqegy6LzpRunQ6lvq5etw6/vshu0R7ZzuKO6070DvzPBY8OXxcvH/8ozzGfOn9DT0w
    vVQ9d72bfb794r4Gfio+Tj5x/pX+uf7d/wH/Jj9Kf26/kv+3P9t////2wBDAAIBAQEBAQIBAQE
    CAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/2
    wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgo
    KCgoKCgoKCgoKCgr/wgARCAAWAA4DAREAAhEBAxEB/8QAFwAAAwEAAAAAAAAAAAAAAAAABQYHC
    P/EABgBAAMBAQAAAAAAAAAAAAAAAAMEBQAC/9oADAMBAAIQAxAAAAGzK1Gugk7YRbseNqDtEIt
    //8QAGRABAAMBAQAAAAAAAAAAAAAABgQFBwID/9oACAEBAAEFAkI4LFV5oVKwb1TB8UEk33C4r
    2e41dSwxHV4zZX/AP/EACMRAAAFBAICAwAAAAAAAAAAAAECAwQFABESMUFRBmETIeH/2gAIAQM
    BAT8BhYFrMKKAY+Jg+9XuHe+6fR7eOkDopDljYL++Q51SS6zdYDomxMHNAN6ivIm0OdTJDMwju
    /4NOpNvJvxVSS+O4a996Cv/xAApEQABAgUDAgYDAAAAAAAAAAABAhEDBAYhMQAFEgcyEyJBQmG
    BFHGR/9oACAECAQE/Aau6k1HSG3SapbkqEQUE8uPFSSSE9pyghv0R7dSVVb1U9My8xPuOalKCS
    X8valWBnzN8XwdKk5OakVpnUBcJVuJ9xF/rjl/rBOpqGpCgrKTizWxj0ZmYWDWs2qg6Q7vW23y
    a4e4+DDEPs4EuVKKnLKD2UB8aVQu40ZTMKBNzf5DRCxYiyki1yp24fy3pr//EACwQAAEDAgMGB
    QUAAAAAAAAAAAECAwQFEQASEwYUISIxYRU0QUKjgpGTobH/2gAIAQEABj8Cqaq3sBBkvS5W8tv
    OKPOhSEXP5A5/fXEyubP7KM0+0RuOVM3spRUpahx7aX3w1Q2GxvLY1jKI8ug3H1ZrEZexPtGPD
    IsNMZcM6b8ULzaauvX3XvmzdTfjxuMVqkuUuZyVVQVkcFlFCENX+P8AffEymtQX05aWg6rywTZ
    Dhsn5Tj//xAAdEAEBAAIDAAMAAAAAAAAAAAABESExAEFhUYGR/9oACAEBAAE/ITyougKJpyz09
    SP5o9AJupjS0QPOG5jvsMumbkX4wVzpfcEhdkEkXJOvDkpCpDMp2uOhQYh0D9r5iHP/2gAMAwE
    AAgADAAAAEFw8P//EABwRAQEAAwEBAQEAAAAAAAAAAAERACExQVFxgf/aAAgBAwEBPxA7yQHQI
    8OCJNUfcPCAgJ9QvoDvtHZiwqoOg6f28n96GPd7d1rXdX29rt93n35CBAAgMqisS6vMiqBQiIW
    6AWlJ0Xrn/8QAGxEBAQEAAgMAAAAAAAAAAAAAAREhADFBUXH/2gAIAQIBAT8QgG2GFQ7KLXQXa
    PO9u8SioMkngcVVOwtiMPvYjuhsdSQiwGcAcPywspK8cwCh1YAo4Yzl9ot6SVVRRpEAg5//xAA
    YEAEBAQEBAAAAAAAAAAAAAAABESEAQf/aAAgBAQABPxDcZMB9hHYcagIeHZ5TIiEwHNUU5KhGR
    ALmCGElI6M1E7oNriiQ711ZUYcJF4AWGQPR53GGhHBYSwIFv//Z'''

    def __init__(self, config_name=''):
        self.config_name = 'ibg-alarm-clock_' + str(config_name) + '.cfg'
        self._get_text()

        print(self.config_name)

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
        if language == 'ru_RU':
            self.texts = ru_text
        else:
            self.texts = en_text

    def _get_config():
        pass

    @staticmethod
    def _setup(icon):
        icon.visible = True

    def tray_exit():
        self.tray_icon.stop()
        sys.exit()


def main():
    clock = AlarmClock()
    # jpg_bytes = base64.b64decode(_IMG_CLOCK_14_22_BASE64.encode())
    # f = io.BytesIO(jpg_bytes)
    # _IMG_CLOCK_14_22 = Image.open(f)
    # tray_menu = pystray.Menu(pystray.MenuItem(texts['open_window'],
    #                                           tray_exit),
    #                          pystray.MenuItem(texts['exit'], tray_exit)
    #                          )
    # tray_icon = pystray.Icon(texts['porgam_name'], icon=_IMG_CLOCK_14_22,
    #                          menu=tray_menu)
    # tray_icon.run(setup)


if __name__ == '__main__':
    try:
        root = Tk()
        del root
    except Exception as a:
        print('Please run the program from GUI-interface')
        sys.exit()
    main()
