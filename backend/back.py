import yfinance as yf
import time


HOLDINGS = 0
CASH = 0

def get_current_price(ticker):
    data = yf.Ticker(ticker)
    price = data.history(period='1d').iloc[-1]['Close']
    return price

def get_current_per(ticker):
    return yf.Ticker(ticker).info.get('trailingPE')

def get_current_roe(ticker):
    return yf.Ticker(ticker).info.get('returnOnEquity')

def get_current_eps(ticker):
    return yf.Ticker(ticker).info.get('trailingEps')

def get_marketCap(ticker):
    return yf.Ticker(ticker).info.get('marketCap')

def get_sector(ticker):
    return yf.Ticker(ticker).info.get('sector')

def get_industry(ticker):
    return yf.Ticker(ticker).info.get('industry')

def buy(price, amount):
    global HOLDINGS, CASH
    shares = int(amount / price)
    if shares > 0 and price * shares <= CASH:
        HOLDINGS += shares
        CASH -= shares * price
        print(f"[BUY] {shares} shares @ ${price:.2f} | Balance: ${CASH:.2f}")

def sell(price):
    global HOLDINGS, CASH
    if HOLDINGS > 0:
        CASH += HOLDINGS * price
        print(f"[SELL] {HOLDINGS} shares @ ${price:.2f} | Balance: ${CASH:.2f}")
        HOLDINGS = 0

def run_bot():
    global HOLDINGS, CASH
    TICKER = input("Insert ticker symbol (e.g., AAPL): ").upper()
    if TICKER == 'Q':
        return

    try:
        BUY_THRESHOLD = float(input("Insert buy threshold: "))
        SELL_THRESHOLD = float(input("Insert sell threshold: "))
        HOLDINGS = int(input("Insert current number of shares: "))
        CASH = float(input("Insert current cash amount ($): "))
    except ValueError:
        print("Wrong number format.")
        return

    print("\n[Bot Started] Press Ctrl+C to stop.")
    try:
        while True:
            try:
                price = get_current_price(TICKER)
                ROE = get_current_roe(TICKER)
                PER = get_current_per(TICKER)
                EPS = get_current_eps(TICKER)
                Cap = get_marketCap(TICKER)
                indu = get_industry(TICKER)
                sect = get_sector(TICKER)

                print(f"\n[Info] {TICKER} price: ${price:.2f} | Holdings: {HOLDINGS} | Cash: ${CASH:.2f}")
                print(f"PER: {PER} | ROE: {ROE} | EPS: {EPS} | Market Cap: ${Cap} | Industry: {indu} | Sector: {sect}")

                if price < BUY_THRESHOLD and CASH >= price:
                    buy(price, CASH * 0.5)  # 50% 자금으로 매수
                elif price > SELL_THRESHOLD and HOLDINGS > 0:
                    sell(price)

                time.sleep(60)
            except Exception as e:
                print(f"[Error] {e}")
                time.sleep(60)
    except KeyboardInterrupt:
        print("\n[Bot Stopped]")

if __name__ == "__main__":
    run_bot()
