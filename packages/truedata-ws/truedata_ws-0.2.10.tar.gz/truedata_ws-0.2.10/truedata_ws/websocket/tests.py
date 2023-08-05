from truedata_ws.websocket.TD import TD
from copy import deepcopy
from time import sleep

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from colorama import Style, Fore, init

DEFAULT_LIVE_PORT = 8082
DEFAULT_HIST_PORT = 8092

init()


def run_all_tests(username, password, live_port=None, historical_port=None, symbols_to_test=None):
    if live_port is None:
        print(f'{Style.BRIGHT}{Fore.BLUE}Setting to default live port = {DEFAULT_LIVE_PORT}{Style.RESET_ALL}')
        live_port = DEFAULT_LIVE_PORT
    if historical_port is None:
        print(f'{Style.BRIGHT}{Fore.BLUE}Setting to default hist port = {DEFAULT_HIST_PORT}{Style.RESET_ALL}')
        historical_port = DEFAULT_HIST_PORT
    if symbols_to_test is None:
        symbols_to_test = ['BANKNIFTY-I', 'NIFTY-I', 'CRUDEOIL-I']

    print(f'{Style.BRIGHT}{Fore.BLUE}Beginning connection test...{Style.RESET_ALL}')
    td_app = get_connection(username, password, live_port, historical_port)

    print(f'{Style.BRIGHT}{Fore.BLUE}Beginning historical data test...{Style.RESET_ALL}')
    run_historical_tests(td_app, symbols_to_test)

    print(f'{Style.BRIGHT}{Fore.BLUE}Beginning live data test...{Style.RESET_ALL}')
    run_live_tests(td_app, symbols_to_test)


def get_connection(username, password, live_port_ip, historical_port_ip):
    td_app = TD(username, password, live_port=live_port_ip, historical_port=historical_port_ip)
    return td_app


def run_historical_tests(td_app_ip, symbols):
    symbol = symbols[0]
    test_time = datetime.today()
    # Testing malformed historical contracts
    # hist_data_0 = td_app_ip.get_historic_data(f'BANKNIFTY99ZYXFUT')

    # Testing bar historical data
    hist_data_1 = td_app_ip.get_historic_data(f'{symbol}')
    hist_data_2 = td_app_ip.get_historic_data(f'{symbol}', duration='3 D')
    hist_data_3 = td_app_ip.get_historic_data(f'{symbol}', duration='3 D', bar_size='15 mins')
    hist_data_4 = td_app_ip.get_historic_data(f'{symbol}', bar_size='30 mins')
    hist_data_5 = td_app_ip.get_historic_data(f'{symbol}', bar_size='30 mins', start_time=test_time-relativedelta(days=3))
    # Testing tick historical data
    tick_hist_data_1 = td_app_ip.get_historic_data(f'{symbol}', bar_size='tick')
    tick_hist_data_2 = td_app_ip.get_historic_data(f'{symbol}', bar_size='tick', duration='3 D')
    tick_hist_data_3 = td_app_ip.get_historic_data(f'{symbol}', bar_size='tick', start_time=test_time-relativedelta(days=3))

    print(f'{Style.BRIGHT}{Fore.BLUE}------------- HIST BAR DATA TEST RESULTS -------------{Style.RESET_ALL}')
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 1...\n"
          f"\tCommand used -> hist_data_1 = td_app.get_historic_data('{symbol}')\n"
          f"\tLENGTH OF RESULT = {len(hist_data_1)}{Style.RESET_ALL}")
    for hist_point in hist_data_1[-20:]:
        print(hist_point)
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 2...\n"
          f"\tCommand used -> hist_data_2 = td_app.get_historic_data('{symbol}', duration='3 D')\n"
          f"\tLENGTH OF RESULT = {len(hist_data_2)}{Style.RESET_ALL}")
    for hist_point in hist_data_2[-20:]:
        print(hist_point)
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 3...\n"
          f"\tCommand used -> hist_data_3 = td_app.get_historic_data('{symbol}', duration='3 D', bar_size='15 mins')\n"
          f"\tLENGTH OF RESULT = {len(hist_data_3)}{Style.RESET_ALL}")
    for hist_point in hist_data_3[-20:]:
        print(hist_point)
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 4...)\n"
          f"\tCommand used -> hist_data_4 = td_app.get_historic_data('{symbol}', bar_size='30 mins')\n"
          f"\tLENGTH OF RESULT = {len(hist_data_4)}{Style.RESET_ALL}")
    for hist_point in hist_data_4[-20:]:
        print(hist_point)
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 5...\n"
          f"\tCommand used -> hist_data_5 = td_app.get_historic_data('{symbol}', bar_size='30 mins', start_time={test_time - relativedelta(days=3)})\n"
          f"\tLENGTH OF RESULT = {len(hist_data_5)}{Style.RESET_ALL}")
    for hist_point in hist_data_5[-20:]:
        print(hist_point)
    print()
    print()
    print(f'{Style.BRIGHT}{Fore.BLUE}------------- HIST TICK DATA TEST RESULTS -------------{Style.RESET_ALL}')
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}TICKDATA 1...\n"
          f"\tCommand used -> tick_data_1 = td_app.get_historic_data('{symbol}', bar_size='tick')\n"
          f"\tLENGTH OF RESULT = {len(tick_hist_data_1)}{Style.RESET_ALL}")
    for hist_point in tick_hist_data_1[-20:]:
        print(hist_point)
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}TICKDATA 2...\n"
          f"\tCommand used -> tick_data_2 = td_app.get_historic_data('{symbol}', bar_size='tick', duration='3 D')\n"
          f"\tLENGTH OF RESULT = {len(tick_hist_data_2)}{Style.RESET_ALL}")
    for hist_point in tick_hist_data_2[-20:]:
        print(hist_point)
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}TICKDATA 3...\n"
          f"\tCommand used -> tick_data_3 = td_app.get_historic_data('{symbol}', bar_size='tick', start_time={test_time - relativedelta(days=3)})\n"
          f"\tLENGTH OF RESULT = {len(tick_hist_data_3)}{Style.RESET_ALL}")
    for hist_point in tick_hist_data_3[-20:]:
        print(hist_point)

    # Testing conversion to pandas dataframe
    print(f'{Style.BRIGHT}{Fore.BLUE}Converting HISTDATA 1 to a Pandas DataFrame{Style.RESET_ALL}')
    print(f'Command used -> df = pd.DataFrame(hist_data_1)')
    df = pd.DataFrame(hist_data_1)
    print(df)
    print(f'{Style.BRIGHT}{Fore.BLUE}Converting TICKDATA 1 to a Pandas DataFrame{Style.RESET_ALL}')
    print(f'Command used -> df = pd.DataFrame(tick_hist_data_1)')
    df = pd.DataFrame(tick_hist_data_1)
    print(df)


def run_live_tests(td_app_ip, symbols):
    # Testing Live data
    # td_app.start_live_data(f'BANKNIFTY{sys.argv[3]}FUTbk')
    print(f'{Style.BRIGHT}{Fore.BLUE}Checking LIVE data streaming...{Style.RESET_ALL}')
    req_ids = td_app_ip.start_live_data(symbols)
    sleep(3)
    print(f"{Style.BRIGHT}{Fore.BLUE}Here's the touchline data...{Style.RESET_ALL}")
    for req_id in req_ids:
        print(td_app_ip.touchline_data[req_id])
    print()
    print(f"{Style.BRIGHT}{Fore.BLUE}Here's the LIVE stream...{Style.RESET_ALL}")
    live_data_objs = {}
    for req_id in req_ids:    
        live_data_objs[req_id] = deepcopy(td_app_ip.live_data[req_id])
    while True:
        for req_id in req_ids:
            if live_data_objs[req_id] != td_app_ip.live_data[req_id]:
                print(td_app_ip.live_data[req_id])
                live_data_objs[req_id] = deepcopy(td_app_ip.live_data[req_id])
