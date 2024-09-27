import json
import redis
import datetime as dt
from configparser import ConfigParser
from fugle_marketdata import WebSocketClient, RestClient

from quote.qmonitor import QuotesMonitor

class MTXMonitor():

    def __init__(self) -> None:
        config = ConfigParser()
        config.read('./config.ini')
        my_api_key = config['Quotes']['Key']
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.redis_client = redis.Redis(connection_pool=pool)
        self.client = WebSocketClient(api_key=my_api_key)
        self.futopt = self.client.futopt

    def handle_message(self, message):
        msg_dict = json.loads(message)
        print(msg_dict)
        if 'event' in msg_dict and msg_dict['event'] == 'data':
            print(f'data: {msg_dict}')
            self.redis_client.publish('mtx', str(msg_dict['data']))
        elif 'event' in msg_dict and msg_dict['event'] == 'snapshot':
            print(f'snapshot: {msg_dict}')
            self.redis_client.publish('mtx', str(msg_dict['data']))
        else:
            print(msg_dict)

    def write_messageq_to_file(self):
        quote_queue = []
        sub = self.redis_client.pubsub()
        sub.subscribe('mtx')
        for message in sub.listen():
            if message['type'] == 'message':
                print(message['data'])
                self.redis_client.rpush('mtx', message['data'])
                json_data = json.dumps(message['data'])
                quote_queue.append(json_data)
            elif message['type'] == 'subscribe':
                print('subscribed')

        file_timemark = dt.now().strftime('%Y%m%d_%H%M%S')
        with open(f'./{file_timemark}.json', 'a') as f:
            f.write(str(quote_queue))
        print('file written')

    def run(self):
        qm = QuotesMonitor()
        target_symbol = qm.get_mtx_symbol()
        print(target_symbol)
        self.futopt.on('message', self.handle_message)
        self.futopt.connect()
        self.futopt.subscribe({
            'channel': 'trades',
            'symbol': target_symbol,
            'afterHours': True
        })
