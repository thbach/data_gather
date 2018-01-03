import ccxt
import csv
import time
import datetime

filename = 'data-{}.csv'.format(datetime.date.today())
sleeptime = 30

with open(filename, 'a', newline='') as csvfile:
    fieldnames = ['exchange', 'timestamp', 'symbol', 'bid', 'ask', 'last']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


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
    'kraken',
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

    result = {}
    result['exchange'] = exchange.name
    result['symbol'] = symbol
    result['timestamp'] = int(ticker['timestamp'])

    if exchange.id == 'huobipro':
        result['bid'] = ticker['info']['bid'][0]
        result['ask'] = ticker['info']['ask'][0]
        result['last'] = 0
    else:
        result['bid'] = ticker['bid']
        result['ask'] = ticker['ask']
        result['last'] = ticker['last']

    return result


exchange_objects = []
for ex in exchanges:
    ex = getattr(ccxt, ex)()
    ex.enableRateLimit = True
    ex.rateLimit = 3000
    ex.load_markets()
    exchange_objects.append(ex)

while True:
    for symbol in symbols:
        with open(filename, 'a', newline='') as csvfile:

            for exchange in exchange_objects:
                if symbol in exchange.symbols:
                    try:
                        ticker = get_ticker(exchange, symbol)

                        fieldnames = ['exchange', 'timestamp', 'symbol', 'bid', 'ask', 'last']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow(ticker)

                        print(ticker)

                    except Exception as e:
                        print(e)
                    # logging.info(ticker)

        print('sleeping')
        time.sleep(30)
