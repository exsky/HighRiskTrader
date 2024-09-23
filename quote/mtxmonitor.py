import json
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
