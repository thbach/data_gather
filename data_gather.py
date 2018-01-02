import ccxt
import logging
import time

logging.basicConfig(
    filename='data_gather.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

exchanges = [
    'binance',
    'bitbay',
    'bitfinex',
    'bitflyer',
    'bitstamp',
    'bittrex',
    'btcmarkets',
    'gdax',
    'hitbtc',
    'huobipro',
    'poloniex',
    'quadrigacx',
]
# 'kraken'

symbols = [
    'BTC/USD',
    'ETH/USD',
    'BCH/USD',
    'XRP/USD',
    'LTC/USD',
    'BTC/CAD',
    'ETH/CAD',
    'BCH/CAD',
    'XRP/CAD',
    'LTC/CAD',
    'BTC/AUD',
    'ETH/AUD',
    'BCH/AUD',
    'XRP/AUD',
    'LTC/AUD',
    'XRP/BTC',
    'ETH/BTC',
    'BCH/BTC',
    'ADA/BTC',
    'LTC/BTC',
    'IOTA/BTC',
    'NEM/BTC',
    'XLM/BTC',
    'XVG/BTC',
    'LSK/BTC',
    'ETC/BTC',
    'QTUM/BTC',
    'BTG/BTC',
    'NEO/BTC',
    'EOS/BTC',
    'XMR/BTC',
    'DASH/BTC'
]


def get_ticker(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    result = {
        'exchange': exchange.id,
        'symbol': symbol,
        'datetime': ticker['datetime'],
        'bid': ticker['bid'],
        'ask': ticker['ask'],
        'last': ticker['last'],
    }

    return result


# print(temp)
exchange_objects = []
for ex in exchanges:
    ex = getattr(ccxt, ex)()
    ex.enableRateLimit = True
    ex.rateLimit = 3000
    ex.load_markets()
    exchange_objects.append(ex)

while True:
    for symbol in symbols:
        for exchange in exchange_objects:
            if symbol in exchange.symbols:
                ticker = get_ticker(exchange, symbol)
                print(ticker)
                logging.info(ticker)

    print('sleeping')
    time.sleep(30)

