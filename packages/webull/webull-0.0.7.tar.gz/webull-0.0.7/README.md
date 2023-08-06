# Webull
APIs for webull, you are free to use, but code not extensively checked and Webull may update the APIs or the endpoints at any time.
https://www.webull.com/


# Install

```
pip install webull
```

# Usage

How to login and get account details
```

from webull import webull # for paper trading, import 'paper-webull'

webull = webull.webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_trade_token('123456') # your 6-digit pin
print(webull.get_account())
```

How to order stock
```
from webull import webull
webull = webull.webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_trade_token('123456')
webull.place_order('NDAQ', 90.0, 2) //stock_ticker_symbol, price, quantity
```

How to check standing orders
```
from webull import webull
webull = webull.webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_trade_token('123456')
orders = webull.get_current_orders()
for order in orders :
  print(order)
```

How to cancel standing orders
```
from webull import webull
webull = webull.webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_trade_token('123456')
orders = webull.get_current_orders()
for order in orders :
  if order['statusCode'] == 'Working' :
    webull.cancel_order(order['orderId'])
```

# Stream Quotes
https://github.com/tedchou12/webull/wiki/How-to-use-Streaming-Quotes%3F

# Disclaimer
This software is not extensively tested, please use at your own risk.

# Developers
If you are interested to join and help me improve this, feel free to message me.
