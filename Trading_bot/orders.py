# Trading SELL order
symbol_tick = mt.symbol_info_tick(symbol)
price = symbol_tick.bid
deviation = 20
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt.ORDER_TYPE_SELL,
    "price": price,
    "tp": price - 100 * 0.001,
    "sl": price + 100 * 0.001,
    "comment": "Trading bot GBPCHF",
    "type_time": mt.ORDER_TIME_GTC,
    "type_filling": mt.ORDER_FILLING_IOC
}
 
# send a trading request
orderSell = mt.order_send(request)
orderSell

# Trading BUY order 
symbol_tick = mt.symbol_info_tick(symbol)
price = symbol_tick.ask
deviation = 20
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * 0.001,
    "tp": price + 100 * 0.001,
    "comment": "Trading bot GBPCHF",
    "type_time": mt.ORDER_TIME_GTC,
    "type_filling": mt.ORDER_FILLING_IOC
}
 
# send a trading request
orderBuy = mt.order_send(request)
orderBuy

# Trading Close position for BUY ORDERS
symbol_tick = mt.symbol_info_tick(symbol)
price = symbol_tick.bid
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt.ORDER_TYPE_SELL,
    "position": 496580955,
    "price": price,
    "comment": "Close position",
    "type_time": mt.ORDER_TIME_GTC,
    "type_filling": mt.ORDER_FILLING_IOC,
}

closePosition = mt.order_send(request)
closePosition

# Trading Close position for SELL ORDERS
symbol_tick = mt.symbol_info_tick(symbol)
price = symbol_tick.ask
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt.ORDER_TYPE_BUY,
    "position": 496585444,
    "price": price,
    "comment": "Close position",
    "type_time": mt.ORDER_TIME_GTC,
    "type_filling": mt.ORDER_FILLING_IOC,
}

closePosition = mt.order_send(request)
closePosition