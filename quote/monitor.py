import json
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
                session='AFTERHOURS', contractType='I')
        return products

    def get_ticker(self, session=None, contractType=None, product=None):
        if session is None:
            session = 'REGULAR'
        if contractType is None:
            contractType = 'I'
        if product is None:
            product='TXF'
        '''
        類型，可選 FUTURE 期貨 ； OPTION 選擇權
        交易時段，可選 REGULAR 一般交易 或 AFTERHOURS 盤後交易
        契約類別，可選 I 指數類；R 利率類；B 債券類；C 商品類；S 股票類；E 匯率類
        契約狀態，可選 N 正常；P 暫停交易；U 即將上市
        product MXF小台 MX4小台w4 TXF大台
        '''
        tickers = self.futopt.intraday.tickers(
                type='FUTURE', exchange='TAIFEX',
                session='AFTERHOURS', contractType='I', product='TXF')
        return tickers

    def get_mtx_quote(self, symbol=None):
        if symbol is None:
            symbol = 'MTX'
        mtx_quote = self.futopt.intraday.quote(symbol='TXF')
        return mtx_quote