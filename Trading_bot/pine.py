# Building a strategy using multiple technical indicators
# 1. EMA
# 2. RSI + MFI
# STop Loss and Target value
# Plot

# This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https:#mozilla.org/MPL/2.0/
# © ngoquocdat093

#@version=5
strategy("My Simple Strategy", overlay = true, initial_capital = 100000, default_qty_type = strategy.percent_of_equity)

# EMA
ema_input1 = input.int(200, 'EMA Length')
ema_ = ta.ema(close, ema_input1)

# trading logic
ema_buy_condition = ema_ < close
ema_sell_condition = ema_ > close

# RSI and MSI indicator (RM indicator)
ma(source, length, type) => 
    switch type 
        "SMA" => ta.sma(source, length)
        "Bollinger Bands" => ta.sma(source, length)
        "EMA" => ta.sma(source, length)
        "SMMA (RMA)" => ta.rma(source, length)
        "WMA" => ta.wma(source, length)
        "VWMA" => ta.vwma(source, length)

rsiLengthInput = input.int(14, minval=1, title="RSI Length", group="RSI Settings")
rsiSourceInput = input.source(close, "Source", group="RSI Settings")
maTypeInput = input.string("SMA", title="MA Type", options=["SMA","Bollinger Bands","EMA","SMM (RMA)","WMA","VWMA"], group="MA Settings")
maLengthInput = input.int(14, title="MA Length", group="MA Settings")
bbMultInput = input.float(2.0, minval=0.001, maxval=50, title="BB StdDev", group="MA Settings")

up = ta.rma(math.max(ta.change(rsiSourceInput), 0), rsiLengthInput)
down = ta.rma(-math.min(ta.change(rsiSourceInput), 0), rsiLengthInput)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

# MFI
length = input.int(title="Length", defval=14, minval=1, maxval=2000)
src = hlc3
mf = ta.mfi(src, length)

rsi_mfi = (rsi+mf)/2

rm_sell_condition = (rsi_mfi >=70)
rm_buy_condition = (rsi_mfi <= 40)


# Stop loss and target price
percent_based = input.float(10.0, "% Stop Multipler", minval=0.0, step=0.5)
r_ratio = input.float(2.0, "Risk Reward ratio", minval=0.0, step=0.5)
stop_loss_amount = close * percent_based/100

bought = strategy.position_size[0] > strategy.position_size[1]
since_entry_long = ta.barssince(bought)
sold = strategy.position_size[0] < strategy.position_size[1]
since_entry_short = ta.barssince(sold)


# Declare variables
price_stop_long = 0.0
price_stop_short = 1000000000.0
targetvalue_long_1 = 0.0
targetvalue_short_1 = 0.0
stopvalue_long = 0.0
stopvalue_short = 0.0

if (strategy.position_size > 0)
    stopvalue_long := close - stop_loss_amount
    price_stop_long := close[since_entry_long] - stop_loss_amount[since_entry_long]
    targetvalue_long_1 := close[since_entry_long] + close[since_entry_long]*(percent_based/100)*r_ratio
else
    price_stop_long := 0.0

if (strategy.position_size < 0)
    stopvalue_short := close - stop_loss_amount
    price_stop_short := close[since_entry_short] - stop_loss_amount[since_entry_short]
    targetvalue_short_1 := close[since_entry_short] + close[since_entry_short]*(percent_based/100)*r_ratio
else
    price_stop_short := 1000000000.0
    
# Excuting trades
if (ema_buy_condition == true) and (rm_buy_condition == true)
    strategy.entry("Long", strategy.long, qty = 1000, when = strategy.position_size <= 0)

if (ema_sell_condition == true) and (rm_sell_condition == true)
    strategy.entry("Short", strategy.short, qty = 1000, when = strategy.position_size >= 0)


# Stop loass and target price trading logics
strategy.exit('Long Exit', from_entry = 'Long', limit = targetvalue_long_1, stop = price_stop_long, when = strategy.position_size > 0)
strategy.exit('Short Exit', from_entry = 'Short', limit = targetvalue_short_1, stop = price_stop_short, when = strategy.position_size < 0)


# Plots
P1 = plot(price_stop_long > 0 ? price_stop_long : na, "SL Long", color = color.purple, style = plot.style_linebr)
P2 = plot(price_stop_long > 0 ? targetvalue_long_1 : na, "Target Long", color = color.aqua, style = plot.style_linebr)

P3 = plot(price_stop_short < 1000000000.0 ? price_stop_short : na, "SL Short", color = color.purple, style = plot.style_linebr)
P4 = plot(price_stop_short < 1000000000.0 ? targetvalue_short_1 : na, "Target Short", color = color.aqua, style = plot.style_linebr)

plot(ema_)
