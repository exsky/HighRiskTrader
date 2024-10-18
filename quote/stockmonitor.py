import json
from datetime import datetime
from configparser import ConfigParser
from fugle_marketdata import WebSocketClient, RestClient


class StockMonitor():

    def __init__(self) -> None:
        config = ConfigParser()
        config.read('./config.ini')
        my_api_key = config['Quotes']['Key']
        self.rclient = RestClient(api_key=my_api_key)
        self.wclient = WebSocketClient(api_key=my_api_key)
        self.stock = self.wclient.stock

        # 一邊讀檔一邊訂閱，還需要避免讀檔失敗，所以採取先讀檔後訂閱
        self.sub_stocks = None
        # 為了讓人類方便讀取，顯示在畫面上的資料，要爬出來
        self.stocks_info = {}
        # 去讀檔知道使用者想看哪幾檔股票
        self.fetch_booking()
        # 去爬股票名字，記錄在字典裡面
        self.grab_stock_info()

        self.start_listen()

    def start_listen(self):
        self.stock.on("connect", self.handle_connect)
        self.stock.on("message", self.handle_message)
        self.stock.on("disconnect", self.handle_disconnect)
        self.stock.on("error", self.handle_error)
        self.stock.connect()
        for sub_stock in self.sub_stocks:
            self.stock.subscribe(sub_stock)

    def fetch_booking(self):
        with open('booking.json', 'r') as file:
            stocks = json.load(file)
        self.sub_stocks = []
        for stock in stocks:
            print(stock)
            self.sub_stocks.append(stock)

    def grab_stock_info(self):
        for sub_stock in self.sub_stocks:
            stock_id = sub_stock['symbol']
            resp = self.rclient.stock.intraday.ticker(symbol=stock_id)
            self.stocks_info[stock_id] = resp

    def handle_message(self, message):
        msg = json.loads(message)
        print(f'{msg["data"]}')
        if "symbol" in msg["data"] and "time" in msg["data"]:
            # 【名稱】成交時間 / 成'price' / 單量'size'
            stock_ch_name = self.stocks_info[msg["data"]["symbol"]]["name"]
            ts = datetime.fromtimestamp(msg["data"]["time"]/1000000)
            msg_time = ts.strftime('%F %T.%f')[:-3]
            print(f'【{stock_ch_name}】 {msg_time}')

            size = msg["data"]["size"]
            price = msg["data"]["price"]
            bid = msg["data"]["bid"]
            ask = msg["data"]["ask"]
            if price >= ask:
                print(f'〖{bid}〗 ->【{ask}】/ 單x {size}')
            elif price <= bid:
                print(f'【{bid}】<- 〖{ask}〗/ 單x {size}')
            else:
                print('lock')

    def handle_connect(self):
        print('connected')


    def handle_disconnect(self, code, message):
        print(f'disconnect: {code}, {message}')


    def handle_error(self, error):
        print(f'error: {error}')
