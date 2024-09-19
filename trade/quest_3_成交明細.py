from configparser import ConfigParser
from fugle_trade.sdk import SDK
from fugle_trade.order import OrderObject
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)

# 讀取設定檔
config = ConfigParser()
config.read('./config.ini')

# 登入
sdk = SDK(config)
sdk.login()

# 成交明細 -> 可透過以下兩種 function 進行查詢！
transactions = sdk.get_transactions("0d")
print('成交明細：')
print(transactions)

#transactions_by_date = sdk.get_transactions_by_date("2022-10-01", "2023-02-24")
#print(transactions_by_date)
