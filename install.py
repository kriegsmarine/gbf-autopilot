#!/usr/bin/env python

import pip

PACKAGES = {
    'base': [
        'flask',
        'flask_cors',
        'pyautogui',
        'requests',
        'pyopenssl',
    ],
    'win32': ['pywin32'],
    'darwin': ['pyobjc-core', 'pyobjc', 'atomac'],
    'linux': []
}

def install(packages):
    for package in packages:
        pip.main(['install', package])

if __name__ == '__main__':
    from sys import platform

    if platform == 'windows':
        install(PACKAGES['win32'])
    elif platform == 'darwin':
        install(PACKAGES['darwin'])
    else:
        install(PACKAGES['linux'])
    install(PACKAGES['base'])
