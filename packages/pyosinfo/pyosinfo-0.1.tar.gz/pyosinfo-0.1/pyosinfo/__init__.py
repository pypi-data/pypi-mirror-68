__author__ = 'Andrey Komissarov'

import platform


def edition():
    edition = platform.win32_edition()

    if edition == 'Enterprise':
        return 'win10'
    elif edition == 'ServerStandard':
        return 'win_server'
    else:
        return 'other:', edition
