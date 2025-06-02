import yfinance as yf
import time


TICKER = 'AAPL'       
BUY_THRESHOLD = 180.00  
SELL_THRESHOLD = 190.00  
HOLDINGS = 500             
CASH = 10000             

def get_current_price(ticker):
    data = yf.Ticker(ticker)
    price = data.history(period='1d').iloc[-1]['Close']
    return price

def get_current_per(ticker):
    return yf.Ticker(ticker).info.get('trailingPE')

def get_current_roe(ticker):
    return yf.Ticker(ticker).info.get('returnOnEquity')

def get_currrent_eps(ticker):
    return yf.Ticker(ticker).info.get('trailingEps')

def buy(price,amount):
    global HOLDINGS, CASH
    shares = int(amount/int)
    if shares > 0:
        HOLDINGS += shares
        CASH -= shares * price
        print(f"[buy] {shares}shares @ ${price:.2f} | balance: ${CASH:.2f}")

def sell(price):
    global HOLDINGS, CASH
    if HOLDINGS > 0:
        CASH += HOLDINGS * price
        print(f"[sell] {HOLDINGS}shares @ ${price:.2f} | balance: ${CASH:.2f}")
        HOLDINGS = 0

def run_bot():
    while True:
        try:
            price = get_current_price(TICKER)
            print(f"[Information] Current price: ${price:.2f} | Holdings: {HOLDINGS} | Cash: ${CASH:.2f}")

            if price < BUY_THRESHOLD and CASH >= price:
                buy(price, CASH * 0.5)  
            elif price > SELL_THRESHOLD and HOLDINGS > 0:
                sell(price)

            time.sleep(60)
        except KeyboardInterrupt:
            print("End program")
            break
        except Exception as e:
            print(f"[error] {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()


