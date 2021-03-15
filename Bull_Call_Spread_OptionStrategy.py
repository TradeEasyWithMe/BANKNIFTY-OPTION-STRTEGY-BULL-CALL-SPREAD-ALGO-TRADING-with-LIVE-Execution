#!C:\Users\WinWinTrader\AppData\Local\Programs\Python\Python38\python.exe
#Bull Call Spread Options strategy
#https://api.kite.trade/instruments -- download instruments using this.

import logging
from kiteconnect import KiteConnect
import csv
import time
import math
from datetime import datetime, timedelta
import acctkn

att=acctkn.att()
ap=acctkn.atp()

kite = KiteConnect(api_key=ap)
kite.set_access_token(att)

orders = []
WeeklyExpiry = '2021-03-18'
Specify_the_Entry_TIME_HHMM = '1258'
Quantity = 25

def def_place_mkt_order_buy(symbl):
 print("Im inside def_place_mkt_order_buy for: ",symbl)
 try:
    order_id = kite.place_order(tradingsymbol=symbl,variety=kite.VARIETY_REGULAR,
                                 exchange=kite.EXCHANGE_NFO,
                                 transaction_type=kite.TRANSACTION_TYPE_BUY,
                                 quantity=Quantity,
                                 order_type=kite.ORDER_TYPE_MARKET,
                                 product=kite.PRODUCT_MIS,price=None, validity=None, 
                                 disclosed_quantity=None, trigger_price=None, 
                                 squareoff=None, stoploss=None, trailing_stoploss=None, tag=None)
 
    print("Order placed. ID is:", order_id)
    return order_id
 except Exception as e:
    print("exception occured:" + str(e))
def def_place_mkt_order_sell(symbl):
 print("Im inside def_place_mkt_order_sell for: ",symbl)
 
 try:
    order_id = kite.place_order(tradingsymbol=symbl,variety=kite.VARIETY_REGULAR,
                                 exchange=kite.EXCHANGE_NFO,
                                 transaction_type=kite.TRANSACTION_TYPE_SELL,
                                 quantity=Quantity,
                                 order_type=kite.ORDER_TYPE_MARKET,
                                 product=kite.PRODUCT_MIS,price=None, validity=None, 
                                 disclosed_quantity=None, trigger_price=None, 
                                 squareoff=None, stoploss=None, trailing_stoploss=None, tag=None)
 
    print("Order placed. ID is:", order_id)
    return order_id
 except Exception as e:
    print("exception occured:" + str(e))
def ORDER_mkt_order_buy():
    tradingsymbol='NIFTY BANK'
    ohlc=kite.ohlc('NSE:{}'.format(tradingsymbol))
    # WORKING print('printing OHLC:',ohlc)
    # WORKING ohl=ohlc['NSE:{}'.format(tradingsymbol)]['ohlc']
    # WORKING print('printing OHL:',ohl)
    # WORKING openn=ohl['open']
    # WORKING print('printing openn:',openn)
    ltp = ohlc['NSE:{}'.format(tradingsymbol)]['last_price']  
    #ltp = ohlc['last_price']  
    print('\n BANKNIFTY SPOT Price:',ltp)
    #val = 31712.5
    #print(val)
    val = ltp
    val2 = math.fmod(val, 100)
    #print('val2', val2)
    x = val - val2
    abs_val = "{:.0f}".format(x) # to remove .0 string.
    print('\n Identified CE ATM:',"{:.0f}".format(x))
    CE_PRICE = "{}".format("{:.0f}".format(x + 0))
    CE_PRICE_2 = "{}".format("{:.0f}".format(x + 300))
    print('\n Identified CE OTM(ATM+300):',CE_PRICE_2)
    
    with open('instruments.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for column in csv_reader:
            if column[6] == CE_PRICE and column[3] =='BANKNIFTY' and column[5] == WeeklyExpiry and column[9] == 'CE' :

                    #place CALL order
                    ord_id = 100
                    ord_id = def_place_mkt_order_buy(column[2])
                    orders.append(ord_id)
                    print('\n CALL contract BUY  Executed: ',column[2])

                    with open('instruments.csv', 'r') as csv_file:
                        csv_reader = csv.reader(csv_file)
                        next(csv_reader)
                    
                        for column in csv_reader:
                            if column[6] == CE_PRICE_2 and column[3] =='BANKNIFTY' and column[5] == WeeklyExpiry and column[9] == 'CE' :
                                    time.sleep(5)
                                    #place CALL order
                                    ord_id = 200
                                    ord_id = def_place_mkt_order_sell(column[2])
                                    orders.append(ord_id)
                                    print('\n CALL contract SELL executed: ',column[2])

    print('\n The Executed order IDs are : ', orders)

####################-------------------------------------------------------MAIN PROGRAM--------------------------------------------------

def Bull_Call_Spread_OptionStrategy():

  print("\n Current time: ",datetime.now())
  curr_dt = time.strftime("%Y%m%d", time.localtime())

  set_order_placement_time_first = curr_dt + Specify_the_Entry_TIME_HHMM
  print("\n Order placement TIME configured as : ",set_order_placement_time_first)
  
  while True:

      curr_tm_chk = time.strftime("%Y%m%d%H%M", time.localtime())
      if ( set_order_placement_time_first == curr_tm_chk or curr_tm_chk > set_order_placement_time_first ):
          print("\n The order placement started")
          ORDER_mkt_order_buy()
          break
      else:
          print("\n Going to wait 10 more seconds till: ",set_order_placement_time_first,' & CURRENT TIME IS',datetime.now())
          time.sleep(10)

Bull_Call_Spread_OptionStrategy()

####################-------------------------------------------------------MAIN PROGRAM END--------------------------------------------------