#API created using the yfinance library to check stock prices 
#and buy or sell according to their appreciation or depreciation.

#Created by Cairo Faleiros using artificila inteligence as a guidance. 

from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

# Function to check stock price and decide buy/sell
def check_stock(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="1d")
    if hist.empty:
        return {"error": "No data available for the stock symbol"}
    
    open_price = hist['Open'][0]
    current_price = hist['Close'][0]
    
    change_percentage = ((current_price - open_price) / open_price) * 100
    
    action = "hold"
    if change_percentage >= 10:
        action = "sell"
    elif change_percentage <= -10:
        action = "buy"
    
    return {
        "stock_symbol": stock_symbol,
        "open_price": open_price,
        "current_price": current_price,
        "change_percentage": change_percentage,
        "action": action
    }

@app.route('/check_stock', methods=['GET'])
def stock_check_api():
    stock_symbol = request.args.get('symbol')
    if not stock_symbol:
        return jsonify({"error": "Stock symbol is required"}), 400
    
    result = check_stock(stock_symbol)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
