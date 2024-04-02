import MetaTrader5 as mt5
import pandas as pd
import time
import pytz
from datetime import datetime

from trading_signals import generate_signals

SYMBOL = "GBPCHFm"
login = 123992590
password = "Demo5@211993!"
server = "Exness-MT5Trial7"

def open_order(symbol, volume, order_type, deviation, magic, stop_loss, take_profit):
    tick = mt5.symbol_info_tick(symbol)

    order_dict = {
        "buy": mt5.ORDER_TYPE_BUY,
        "sell": mt5.ORDER_TYPE_SELL
    }

    price_dict = {
        "buy": tick.ask,
        "sell": tick.bid
    }

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": deviation,
        "magic": magic,
        "sl": stop_loss,
        "tp": take_profit,
        "comment": "Trading bot BTCUSD",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    order = mt5.order_send(request)
    return order

def get_signals(symbol, time_frame):
    bars = mt5.copy_rates_from(symbol, time_frame, datetime(2023,7,21), 5)
    bars2 = mt5.copy_rates_from(symbol, time_frame, datetime(2023,7,21), 8)

    bars_df = pd.DataFrame(data=bars)
    bars_df2 = pd.DataFrame(data=bars2)

    print("pd.DataFrame : ", bars_df)
    sma_1 = bars_df.close.mean()
    sma_2 = bars_df2.close.mean()

    if round(sma_1, 5) != round(sma_2, 5):
        if sma_1 > sma_2:
            print("====================================================")
            print("Buy signal")
            print("====================================================")
            return "buy"
        elif sma_1 < sma_2:
            print("====================================================")
            print("Sell signal")
            print("====================================================")
            return "sell"
        return None
    return None

initialize = mt5.initialize()
if initialize:
    mt5.login(login, password, server)
    print("Info: Connected to MetaTrader5")

while True:
    symbol_info = mt5.symbol_info(SYMBOL)
    tick = mt5.symbol_info_tick(SYMBOL)
    number_of_pos = len(list(filter(lambda pos: pos.symbol == SYMBOL, mt5.positions_get())))

    print("====================================================")
    print("Symbol: ", SYMBOL)
    print("Buy Tick:", tick.ask)
    print("Sell Tick: ", tick.bid)

    generate_signals(SYMBOL)

    if number_of_pos < 1:
        signal = get_signals(symbol=SYMBOL, time_frame=mt5.TIMEFRAME_M5)

        if signal == 'buy':
            open_order(
                symbol=SYMBOL, 
                volume=0.01, 
                deviation=10,
                order_type="buy",
                magic=20, 
                stop_loss=tick.ask - 50 * symbol_info.point, 
                take_profit=tick.bid + 50 * symbol_info.point
            )
        elif signal == 'sell':
            open_order(
                symbol=SYMBOL, 
                volume=0.01, 
                deviation=10,
                order_type="sell",
                magic=20, 
                stop_loss=tick.ask - 50 * symbol_info.point, 
                take_profit=tick.bid + 50 * symbol_info.point
            )

    time.sleep(1)