import MetaTrader5 as mt5
import time

def initialize_mt5():
    if not mt5.initialize():
        print("Initialize() failed, error code =", mt5.last_error())
        return False
    return True

def login_mt5(account, password, server):
    authorized = mt5.login(account, password, server)
    if not authorized:
        print("Failed to connect, error code =", mt5.last_error())
        return False
    print("Connected to MT5 account #{}".format(account))
    return True

def fetch_market_data(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    return rates

def place_order(symbol, order_type, lot_size):
    price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": order_type,
        "price": price,
        "deviation": 20,
        "magic": 234000,
        "comment": "Python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    return result

if __name__ == "__main__":
    if initialize_mt5() and login_mt5(12345678, "your_password", "your_broker_server"):
        while True:
            rates = fetch_market_data("EURUSD", mt5.TIMEFRAME_M5, 100)
            # Implement your trading strategy here
            time.sleep(60)  # Run every 60 seconds
