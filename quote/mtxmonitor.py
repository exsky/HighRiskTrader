import json
import datetime as dt
from datetime import timedelta
from configparser import ConfigParser
from fugle_marketdata import WebSocketClient, RestClient

class MTXMonitor():

    def __init__(self) -> None:
        config = ConfigParser()
        config.read('./config.ini')
        my_api_key = config['Quotes']['Key']
        self.client = WebSocketClient(api_key=my_api_key)
        self.futopt = self.client.futopt

    def handle_message(self, message):
        print(message)

    def third_wednesday(self, year, month):
        day = 21-(dt.date(year, month, 1).weekday()+4)%7
        return dt.date(year, month, day)

    def get_next_expiration(self):
        #now = dt.datetime.now()  # 現在時間；從月期指角度來說，可能是換約前、到期日早盤、到期日夜盤、換約至下個月
        now = dt.datetime(2024, 9, 18, 10, 21, 22)
        next_30_days = now + timedelta(days=30)
        # 輸入今天日期，去看看是不是第三個星期三？
        if now.date() > self.third_wednesday(year=now.year, month=now.month): # 換約至下個月
            mtx_expiration = self.third_wednesday(year=next_30_days.year, month=next_30_days.month)
        elif now.date() <  self.third_wednesday(year=now.year, month=now.month): # 尚未換月
            mtx_expiration = self.third_wednesday(year=now.year, month=now.month)
        else:   # 換約日
            if now.hour > 14:
                mtx_expiration = self.third_wednesday(year=next_30_days.year, month=next_30_days.month)
            else:
                mtx_expiration = self.third_wednesday(year=now.year, month=now.month)
        print(mtx_expiration)
        return mtx_expiration

    def run(self):
        def handle_message(message):
            print(message)
        self.futopt.on('message', handle_message)
        self.futopt.connect()
        self.futopt.subscribe({
            'channel': 'trades',
            'symbol': 'MXFJ4',
            'afterHours': True
        })
