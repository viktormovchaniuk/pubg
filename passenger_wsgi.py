from pyramid.paster import get_app
import sys
import os
virtual_env = os.path.expanduser('~/virtualenv/venv')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')


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


path = '/pubg_project'

if path not in sys.path:
    sys.path.append(path)

ini_path = path + '/production.ini'
application = get_app(ini_path, 'main')
