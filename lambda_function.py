import yfinance as yf
def lambda_handler(event, context):
    if "ticker" in event:
        sp500_data = yf.download(event['ticker'], period="2y", interval="1h")
        return sp500_data
    else:
        return "Send a ticker"