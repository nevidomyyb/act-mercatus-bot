import yfinance as yf

def check_act(act_symbol):
    if '.SA' not in act_symbol:
        act_symbol += '.SA'
    try:
        ticker = yf.Ticker(act_symbol)
        data = ticker.info
        return data
    except:
        return False