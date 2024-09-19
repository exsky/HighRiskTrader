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

# 查詢交割款
settlements = sdk.get_settlements()
print(settlements)
