import sys
from .websocket import tests
from . import __version__

if sys.argv[1] == 'run_all_tests':
    print(f'Running all tests on version = {__version__}')
    username = sys.argv[2]
    password = sys.argv[3]
    try:
        live_port = int(sys.argv[5])
        hist_port = int(sys.argv[6])
    except IndexError:
        live_port = None
        hist_port = None
    tests.run_all_tests(username, password, live_port, hist_port)
