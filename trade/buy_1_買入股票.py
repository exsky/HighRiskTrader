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


# 建立委託物件
order = OrderObject(
    buy_sell = Action.Buy,
    price = inventory['price_evn'],
    stock_no = inventory['stk_no'],
    quantity = 1,
)

sdk.place_order(order)
print("Your order has been placed successfully.")

orderResults = sdk.get_order_results()
print(orderResults)
