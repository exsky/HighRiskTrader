import json
import datetime as dt
from datetime import timedelta
from configparser import ConfigParser
from fugle_marketdata import WebSocketClient, RestClient

class QuotesMonitor():

    def __init__(self) -> None:
        config = ConfigParser()
        config.read('./config.ini')
        my_api_key = config['Quotes']['Key']
        self.client = RestClient(api_key=my_api_key)
        self.futopt = self.client.futopt

    def handle_message(self, message):
        #print(f'message: {message}')
        msg = json.loads(message)
        print(f'{msg["data"]}')

    def handle_connect(self):
        print('connected')

    def handle_disconnect(self, code, message):
        print(f'disconnect: {code}, {message}')

    def handle_error(self, error):
        print(f'error: {error}')

    def get_product(self, session=None, contractType=None):
        if session is None:
            session = 'REGULAR'
        if contractType is None:
            contractType = 'I'
        '''
        類型，可選 FUTURE 期貨 ； OPTION 選擇權
        交易時段，可選 REGULAR 一般交易 或 AFTERHOURS 盤後交易
        契約類別，可選 I 指數類；R 利率類；B 債券類；C 商品類；S 股票類；E 匯率類
        契約狀態，可選 N 正常；P 暫停交易；U 即將上市
        '''
        products = self.futopt.intraday.products(
                type='FUTURE', exchange='TAIFEX',
                session=session, contractType=contractType)
        return products

    def get_ticker(self, session=None, contractType=None, product=None):
        if session is None:
            session = 'REGULAR'
        if contractType is None:
            contractType = 'I'
        if product is None:
            product = 'MXF'
            # product='TXF'
        '''
        類型，可選 FUTURE 期貨 ； OPTION 選擇權
        交易時段，可選 REGULAR 一般交易 或 AFTERHOURS 盤後交易
        契約類別，可選 I 指數類；R 利率類；B 債券類；C 商品類；S 股票類；E 匯率類
        契約狀態，可選 N 正常；P 暫停交易；U 即將上市
        product MXF小台 MX4小台w4 TXF大台
        '''
        tickers = self.futopt.intraday.tickers(
                type='FUTURE', exchange='TAIFEX',
                session=session, contractType=contractType, product=product)
        return tickers

    def third_wednesday(self, year, month):
        day = 21-(dt.date(year, month, 1).weekday()+4)%7
        return dt.date(year, month, day)

    def get_next_expiration(self):
        now = dt.datetime.now()  # 現在時間；從月期指角度來說，可能是換約前、到期日早盤、到期日夜盤、換約至下個月
        #now = dt.datetime(2024, 9, 18, 10, 21, 22)
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
        return mtx_expiration

    def get_mtx_symbol(self):
        now = dt.datetime.now()
        end_date = self.get_next_expiration().strftime("%Y-%m-%d")
        tks = None
        if now.hour > 14 or now.hour < 6:
            tks = self.get_ticker(session='REGULAR', contractType='I', product='MXF')
        else:
            tks = self.get_ticker(session='AFTERHOURS', contractType='I', product='MXF')
        if 'data' not in tks.keys():
            print('no data')
            return None
        for tk in tks['data']:
            if tk['endDate'] == end_date:
                return tk['symbol']