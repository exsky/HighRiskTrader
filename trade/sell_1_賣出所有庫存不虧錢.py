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

# 取得庫存明細
inventories = sdk.get_inventories()

for inventory in inventories:
    # 建立委託物件
    order = OrderObject(
        buy_sell = Action.Sell,
        price = inventory['price_evn'],
        stock_no = inventory['stk_no'],
        quantity = 1,
    )
    #print(order)
    sdk.place_order(order)
    print("Your order has been placed successfully.")

orderResults = sdk.get_order_results()
print(orderResults)
