import config
import csv

from binance import Client, helpers
from flask import flash, redirect

CLIENT = Client(config.API_KEY, config.API_SECRET)


def get_symbols():
    exchange_info = CLIENT.get_exchange_info()
    return exchange_info['symbols']


def get_balance():
    account = CLIENT.get_account()
    return account['balances']


def get_last_prices():
    try:
        FILE_NAME = "current_prices.csv"
        # prices get return has json object and the file is truncated when opened
        tickers = CLIENT.get_all_tickers()
        csvfile = open('data/' + FILE_NAME, 'w')
        csv_writer = csv.writer(csvfile)

        count = 0
        for ticker in tickers:
            if count == 0:
                header = ticker.keys()
                csv_writer.writerow(header)
                count += 1

            csv_writer.writerow(ticker.values())
        csvfile.close()
        flash(FILE_NAME + " was downloaded successfully", "Success")
    except Exception as e:
        flash(e.message if hasattr(e, 'message') else str(e), "Error")
    return redirect('/csv')


def get_1day_interval_report_for_btcusdt():
    try:
        # candles get return as arrays
        FILE_NAME = "BTCUSDT_1day_interval.csv"
        candle_lines = CLIENT.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1DAY)
        csvfile = open('data/' + FILE_NAME, 'w', newline='')
        candlestick_writer = csv.writer(csvfile, delimiter=',')

        for candle in candle_lines:
            candlestick_writer.writerow(candle)

        csvfile.close()
        flash(FILE_NAME + " was downloaded successfully", "Success")
    except Exception as e:
        flash(e.message if hasattr(e, 'message') else str(e), "Error")
    return redirect('/csv')


def get_low_time_frame_data(symbols, date_start, date_end):
    try:
        candle_lines = CLIENT.get_historical_klines(symbols, Client.KLINE_INTERVAL_5MINUTE,
                                                    helpers.convert_ts_str(date_start),
                                                    helpers.convert_ts_str(date_end))

        processed_candlesticks = []

        # lightweight chart expects unix timestamp
        # python-binance helpers coverts str to milliseconds
        # milliseconds divide 1000 = unix timestamp
        for data in candle_lines:
            candlestick = {
                "time": data[0] / 1000,
                "open": data[1],
                "high": data[2],
                "low": data[3],
                "close": data[4]
            }
            processed_candlesticks.append(candlestick)
        flash("Low time frame chart was refreshed", "Success")
    except Exception as e:
        flash(e.message if hasattr(e, 'message') else str(e), "Error")
    return processed_candlesticks


def get_high_time_frame_data(symbols, date_start, date_end):
    try:
        candle_lines = CLIENT.get_historical_klines(symbols, Client.KLINE_INTERVAL_1DAY,
                                                    helpers.convert_ts_str(date_start),
                                                    helpers.convert_ts_str(date_end))

        processed_candlesticks = []

        for data in candle_lines:
            candlestick = {
                "time": data[0] / 1000,
                "open": data[1],
                "high": data[2],
                "low": data[3],
                "close": data[4]
            }
            processed_candlesticks.append(candlestick)
        flash("High time frame chart was refreshed", "Success")
    except Exception as e:
        flash(e.message if hasattr(e, 'message') else str(e), "Error")
    return processed_candlesticks
