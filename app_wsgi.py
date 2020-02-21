import sys
import os
activate_this = '/var/www/u0830336/data/www/matteocs.ru/venv/bin/activate_this.py'


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        '__file__': filepath,
        '__name__': '__main__',
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


execfile(activate_this, dict(__file__=activate_this))

from pyramid.paster import get_app

path = '/var/www/u0830336/data/www/matteocs.ru'

if path not in sys.path:
    sys.path.append(path)

ini_path = path + '/production.ini'
application = get_app(ini_path, 'main')
