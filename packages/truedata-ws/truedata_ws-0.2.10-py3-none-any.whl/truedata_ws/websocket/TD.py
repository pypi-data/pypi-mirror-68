from websocket import WebSocketApp, create_connection
from .support import TickLiveData, TouchlineData

from threading import Thread

from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

from colorama import Style, Fore

DEFAULT_HISTORIC_DATA_ID = 1000
DEFAULT_MARKET_DATA_ID = 2000


class TDHistoricDataError(Exception):
    def __str__(self):
        return f"{Style.BRIGHT}{Fore.RED}Something's wrong with the historical data...{Style.RESET_ALL}"


class TDLiveDataError(Exception):
    def __str__(self):
        return f"{Style.BRIGHT}{Fore.RED}Something's wrong with the historical data...{Style.RESET_ALL}"


class TDInvalidRequestError(Exception):
    def __str__(self):
        return f"{Style.BRIGHT}{Fore.RED}Invalid request{Style.RESET_ALL}"


class LiveClient(WebSocketApp):

    def __init__(self, parent_app, url, on_open=None, *args):
        if on_open is None:
            on_open = self.on_open_func
        WebSocketApp.__init__(self, url, on_open=on_open, on_message=self.on_msg_func, *args)
        self.segments = []
        self.max_symbols = 0
        self.remaining_symbols = 0
        self.valid_until = ''
        self.contract_mapping = {}
        self.parent_app = parent_app

    def on_open_func(self):
        # print(f"Opening WS...")
        pass

    def on_msg_func(self, message):
        msg = json.loads(message)
        if 'message' in msg.keys():
            self.handle_message_data(msg)
        if 'trade' in msg.keys():
            trade = msg['trade']
            self.handle_trade_data(trade)
        elif 'bidask' in msg.keys():
            pass

    def handle_message_data(self, msg):
        # print(f"Truedata has this message for you -> {msg['message']}")
        if msg['message'] == 'TrueData Real Time Data Service':  # Connection success message
            print(f"You have subscribed for {msg['maxsymbols']} symbols across {msg['segments']} until {msg['validity']}...")
        if msg['message'] == 'invalid request':
            print('raising request error')
            raise TDInvalidRequestError
        if msg['message'] == 'symbols added':
            self.add_contract_details(msg['symbollist'])
        if msg['message'] == 'symbols removed':
            pass

    def add_contract_details(self, contracts_list):
        for contract in contracts_list:
            contract_details = contract.split(':')
            self.contract_mapping[int(contract_details[1])] = symbol = contract_details[0]
            for ticker_id in self.parent_app.symbol_mkt_id_map[symbol]:
                self.parent_app.touchline_data[ticker_id].symbol = symbol
                self.parent_app.touchline_data[ticker_id].truedata_id = int(contract_details[1])
                self.parent_app.touchline_data[ticker_id].open = self.parent_app.live_data[ticker_id].day_open = float(contract_details[2])
                self.parent_app.touchline_data[ticker_id].high = self.parent_app.live_data[ticker_id].day_high = float(contract_details[3])
                self.parent_app.touchline_data[ticker_id].low = self.parent_app.live_data[ticker_id].day_low = float(contract_details[4])
                self.parent_app.touchline_data[ticker_id].ltp = float(contract_details[5])
                self.parent_app.touchline_data[ticker_id].prev_close = self.parent_app.live_data[ticker_id].prev_day_close = float(contract_details[6])
                self.parent_app.touchline_data[ticker_id].ttq = int(contract_details[7])
                self.parent_app.touchline_data[ticker_id].oi = int(contract_details[8])
                self.parent_app.touchline_data[ticker_id].prev_oi = self.parent_app.live_data[ticker_id].prev_day_oi = int(contract_details[9])
                self.parent_app.touchline_data[ticker_id].turnover = float(contract_details[10])

    def handle_trade_data(self, trade_tick):
        try:
            symbol = self.contract_mapping[int(trade_tick[0])]
            # print(f'{Style.BRIGHT}{Fore.GREEN} This symbol({symbol}) is tied to req_ids of {self.parent_app.symbol_mkt_id_map[symbol]}...{Style.RESET_ALL}')
            # print(f"{trade_tick} || {type(trade_tick)}")
            for ticker_id in self.parent_app.symbol_mkt_id_map[symbol]:
                # Assigning new data
                self.parent_app.live_data[ticker_id].symbol_id = int(trade_tick[0])
                self.parent_app.live_data[ticker_id].timestamp = datetime.strptime(trade_tick[1], '%Y-%m-%dT%H:%M:%S')  # Old format = '%m/%d/%Y %I:%M:%S %p'
                self.parent_app.live_data[ticker_id].symbol = symbol
                self.parent_app.live_data[ticker_id].ltp = self.parent_app.touchline_data[ticker_id].ltp = ltp = float(trade_tick[2])
                self.parent_app.live_data[ticker_id].volume = float(trade_tick[3])
                self.parent_app.live_data[ticker_id].atp = float(trade_tick[4])
                self.parent_app.live_data[ticker_id].oi = float(trade_tick[5])
                self.parent_app.live_data[ticker_id].ttq = float(trade_tick[6])
                self.parent_app.live_data[ticker_id].special_tag = special_tag = str(trade_tick[7])
                if special_tag != "":
                    if special_tag == 'H':
                        self.parent_app.live_data[ticker_id].day_high = self.parent_app.touchline_data[ticker_id].high = ltp
                    elif special_tag == 'L':
                        self.parent_app.live_data[ticker_id].day_low = self.parent_app.touchline_data[ticker_id].low = ltp
                self.parent_app.live_data[ticker_id].tick_seq = int(trade_tick[8])
                # Calculating addn data
                self.parent_app.live_data[ticker_id].oi_change = self.parent_app.live_data[ticker_id].oi - self.parent_app.live_data[ticker_id].prev_day_oi
                self.parent_app.live_data[ticker_id].oi_change_perc = self.parent_app.live_data[ticker_id].oi_change * 100 / self.parent_app.live_data[ticker_id].prev_day_oi
                self.parent_app.live_data[ticker_id].change = self.parent_app.live_data[ticker_id].ltp - self.parent_app.live_data[ticker_id].prev_day_close
                self.parent_app.live_data[ticker_id].change_perc = self.parent_app.live_data[ticker_id].change * 100 / self.parent_app.live_data[ticker_id].prev_day_close
                try:
                    self.parent_app.live_data[ticker_id].best_bid_price = float(trade_tick[9])
                    self.parent_app.live_data[ticker_id].best_bid_qty = float(trade_tick[10])
                    self.parent_app.live_data[ticker_id].best_ask_price = float(trade_tick[11])
                    self.parent_app.live_data[ticker_id].best_ask_qty = float(trade_tick[12])
                except (IndexError, ValueError, TypeError):
                    del self.parent_app.live_data[ticker_id].best_bid_price
                    del self.parent_app.live_data[ticker_id].best_bid_qty
                    del self.parent_app.live_data[ticker_id].best_ask_price
                    del self.parent_app.live_data[ticker_id].best_ask_qty

        except KeyError:
            print(f'{Style.BRIGHT}{Fore.RED}This symbol is not tied to any req_id...{Style.RESET_ALL}')


class HistoricalWebsocket:
    def __init__(self, login_id, password, url, historical_port):
        self.login_id = login_id
        self.password = password
        self.url = url
        self.historical_port = historical_port
        self.hist_socket = create_connection(f"wss://{self.url}:{self.historical_port}?user={self.login_id}&password={self.password}")
        welcome_msg = self.hist_socket.recv()
        print(f"Connected successfully to '{json.loads(welcome_msg)['message']}'")

    def get_hist_bar_data(self, contract, query_time, start_time, bar_size):
        # print(f'{{"method": "gethistory", "interval": "{bar_size}", "symbol": "{contract}", "from": "{start_time}", "to": "{query_time}"}}')
        self.hist_socket.send(f'{{"method": "gethistory", "interval": "{bar_size}", "symbol": "{contract}", "from": "{start_time}", "to": "{query_time}"}}')
        raw_hist_data = self.hist_socket.recv()
        hist_data = json.loads(raw_hist_data)['data']
        hist_data = self.hist_bar_data_to_dict_list(hist_data, contract)
        return hist_data

    @staticmethod
    def hist_bar_data_to_dict_list(hist_data, contract):  # No need for symbol other than printing
        data_list = []
        count = 0
        for j in hist_data:
            try:  # TODO: Remove HOT-FIX because of this data point ['2020-02-13T09:15:00', 31565.05, 31565.05, 31565.05, 31565.05, 160, None]
                data_list.append({'time': datetime.strptime(j[0], '%Y-%m-%dT%H:%M:%S'),
                                  'o': float(j[1]),
                                  'h': float(j[2]),
                                  'l': float(j[3]),
                                  'c': float(j[4]),
                                  'v': int(j[5]),
                                  'oi': int(j[6])})
            except TypeError:
                print(f'{Style.BRIGHT}{Fore.RED} {contract} erred with {j}...{Style.RESET_ALL} \n\t {hist_data[count-2]} \n\t {hist_data[count-1]} \n\t {hist_data[count]} \n\t {hist_data[count+1]} \n\t {hist_data[count+2]}')
                continue
            count = count + 1
        return data_list

    def get_hist_tick_data(self, contract, query_time, start_time):
        self.hist_socket.send(f'{{"method": "gethistory", "interval": "tick", "symbol": "{contract}", "from": "{start_time}", "to": "{query_time}"}}')
        raw_hist_data = self.hist_socket.recv()
        hist_data = json.loads(raw_hist_data)['data']
        hist_data = self.hist_tick_data_to_dict_list(hist_data, contract)
        return hist_data

    @staticmethod
    def hist_tick_data_to_dict_list(hist_data, contract):
        data_list = []
        count = 0
        for j in hist_data:
            try:  # TODO: Remove HOT-FIX because of any erroneous data points
                data_list.append({'time': datetime.strptime(j[0], '%Y-%m-%dT%H:%M:%S'),
                                  'ltp': float(j[1]),
                                  'volume': int(j[2]),
                                  'oi': int(j[3]),
                                  'bid': float(j[4]),
                                  'bid_qty': int(j[5]),
                                  'ask': float(j[6]),
                                  'ask_qty': int(j[7])})
            except TypeError:
                print(f'{Style.BRIGHT}{Fore.RED} {contract} erred with {j}...{Style.RESET_ALL} \n\t {hist_data[count - 2]} \n\t {hist_data[count - 1]} \n\t {hist_data[count]} \n\t {hist_data[count + 1]} \n\t {hist_data[count + 2]}')
                # If OI is None
                if j[3] is None:
                    prev_datapoint_oi = int(hist_data[count-1][3])
                    data_list.append({'time': datetime.strptime(j[0], '%Y-%m-%dT%H:%M:%S'),
                                      'ltp': float(j[1]),
                                      'volume': int(j[2]),
                                      'oi': prev_datapoint_oi,
                                      'bid': float(j[4]),
                                      'bid_qty': int(j[5]),
                                      'ask': float(j[6]),
                                      'ask_qty': int(j[7])})
                continue
            except IndexError:
                # Missing bid-ask data
                pass
            count = count + 1
        return data_list


class TD:
    def __init__(self, login_id, password, url='push.truedata.in', live_port=8082, historical_port=8092, fyers_token=None, *args):
        self.live_websocket = None
        self.historical_websocket = None
        self.login_id = login_id
        self.password = password
        self.url = url
        self.live_port = live_port
        self.historical_port = historical_port
        if historical_port is None:
            self.connect_historical = False
        else:
            self.connect_historical = True
        self.fyers_token = fyers_token
        self.hist_data = {}
        self.live_data = {}
        self.symbol_mkt_id_map = {}
        self.streaming_symbols = {}
        self.touchline_data = {}
        self.connect()

    def connect(self):
        fyers_append = ''
        if self.fyers_token is not None:
            fyers_append = f'&brokertoken={self.fyers_token}'
        self.live_websocket = LiveClient(self, f"wss://{self.url}:{self.live_port}?user={self.login_id}&password={self.password}{fyers_append}")
        t = Thread(target=self.connect_thread, args=())
        t.start()
        if self.connect_historical:
            self.historical_websocket = HistoricalWebsocket(self.login_id, self.password, self.url, self.historical_port)

    def connect_thread(self):
        self.live_websocket.run_forever()

    def disconnect(self):
        self.live_websocket.close()
        print(f"{Fore.GREEN}Disconnected LIVE TrueData...{Style.RESET_ALL}")
        if self.connect_historical:
            self.historical_websocket.hist_socket.close()
            print(f"{Fore.GREEN}Disconnected HISTORICAL TrueData...{Style.RESET_ALL}")

    @staticmethod
    def truedata_duration_map(regular_format, end_date):
        duration_units = regular_format.split()[1].upper()
        if len(duration_units) > 1:
            raise TDHistoricDataError
        duration_size = int(regular_format.split()[0])
        if duration_units == 'D':
            return (end_date - relativedelta(days=duration_size - 1)).date()
        elif duration_units == 'W':
            return (end_date - relativedelta(weeks=duration_size)).date()
        elif duration_units == 'M':
            return (end_date - relativedelta(months=duration_size)).date()
        elif duration_units == 'Y':
            return (end_date - relativedelta(years=duration_size)).date()

    def get_historic_data(self, contract,
                          ticker_id=DEFAULT_HISTORIC_DATA_ID,
                          query_time=None,
                          duration=None,
                          start_time=None,
                          bar_size="1 min"):
        global DEFAULT_HISTORIC_DATA_ID
        if (duration is None and start_time is None) or (duration is not None and start_time is not None):
            # print(f'Using duration over start time due to ambiguity...')
            return self.get_historical_data_from_duration(contract=contract,
                                                          ticker_id=ticker_id,
                                                          query_time=query_time,
                                                          duration=duration,
                                                          bar_size=bar_size)
        if duration is not None:
            return self.get_historical_data_from_duration(contract=contract,
                                                          ticker_id=ticker_id,
                                                          query_time=query_time,
                                                          duration=duration,
                                                          bar_size=bar_size)
        elif start_time is not None:
            return self.get_historical_data_from_start_time(contract=contract,
                                                            ticker_id=ticker_id,
                                                            query_time=query_time,
                                                            start_time=start_time,
                                                            bar_size=bar_size)

    def get_historical_data_from_duration(self, contract,
                                          ticker_id=DEFAULT_HISTORIC_DATA_ID,
                                          query_time=None,
                                          duration=None,
                                          bar_size="1 min"):
        global DEFAULT_HISTORIC_DATA_ID
        if duration is None:
            duration = "1 D"
        if query_time is None:
            query_time = datetime.today()
        start_time = self.truedata_duration_map(duration, query_time)

        query_time = query_time.strftime('%Y-%m-%d') + 'T23:59:59'
        start_time = start_time.strftime('%Y-%m-%d') + 'T00:00:00'

        if bar_size == 'tick':
            hist_data = self.historical_websocket.get_hist_tick_data(contract, query_time, start_time)
        else:
            bar_size = bar_size.replace(' ', '')
            if bar_size[-1] == 's':
                bar_size = bar_size[:-1]
            hist_data = self.historical_websocket.get_hist_bar_data(contract, query_time, start_time, bar_size)
        DEFAULT_HISTORIC_DATA_ID = DEFAULT_HISTORIC_DATA_ID + 1
        self.hist_data[ticker_id] = hist_data
        return hist_data

    def get_historical_data_from_start_time(self, contract,
                                            ticker_id=DEFAULT_HISTORIC_DATA_ID,
                                            query_time=None,
                                            start_time=None,
                                            bar_size="1 min"):
        global DEFAULT_HISTORIC_DATA_ID
        if query_time is None:
            query_time = datetime.today()
        if start_time is None:
            start_time = datetime.today()

        query_time = query_time.strftime('%Y-%m-%d') + 'T23:59:59'
        start_time = start_time.strftime('%Y-%m-%d') + 'T00:00:00'

        if bar_size == 'tick':
            hist_data = self.historical_websocket.get_hist_tick_data(contract, query_time, start_time)
        else:
            bar_size = bar_size.replace(' ', '')
            if bar_size[-1] == 's':
                bar_size = bar_size[:-1]
            hist_data = self.historical_websocket.get_hist_bar_data(contract, query_time, start_time, bar_size)
        DEFAULT_HISTORIC_DATA_ID = DEFAULT_HISTORIC_DATA_ID + 1
        self.hist_data[ticker_id] = hist_data
        return hist_data

    def start_live_data(self, resolved_contracts, req_id=None):
        global DEFAULT_MARKET_DATA_ID
        if req_id is None:
            req_id = DEFAULT_MARKET_DATA_ID

        req_ids = []
        if type(req_id) == list:
            if len(req_id) == len(resolved_contracts):
                req_ids = req_id
            else:
                print(f"{Style.BRIGHT}{Fore.RED}Lengths do not match...{Style.RESET_ALL}")
        elif req_id is None:
            curr_req_id = DEFAULT_MARKET_DATA_ID
            for i in range(0, len(resolved_contracts)):
                req_ids.append(curr_req_id + i)
            DEFAULT_MARKET_DATA_ID = DEFAULT_MARKET_DATA_ID + len(resolved_contracts)
        elif type(req_id) == int:
            curr_req_id = req_id
            for i in range(0, len(resolved_contracts)):
                req_ids.append(curr_req_id + i)
        else:
            print(f"{Style.BRIGHT}{Fore.RED}Invalid req_id datatype...{Style.RESET_ALL}")
            raise TDLiveDataError
        for j in range(0, len(req_ids)):
            self.touchline_data[req_ids[j]] = TouchlineData()
            self.live_data[req_ids[j]] = TickLiveData(resolved_contracts[j])
            try:
                self.symbol_mkt_id_map[resolved_contracts[j].upper()].append(req_ids[j])
            except KeyError:
                self.symbol_mkt_id_map[resolved_contracts[j].upper()] = [req_ids[j]]
        self.live_websocket.send(f'{{"method": "addsymbol", "symbols": {json.dumps(resolved_contracts)}}}')
        return req_ids

    def stop_live_data(self, contract):
        self.live_websocket.send(f'{{"method": "removesymbol", "symbols": ["{contract}"]}}')
