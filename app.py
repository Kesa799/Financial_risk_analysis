
from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import numpy as np
from quantum_risk import quantum_risk_analysis

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():

    stock = request.form['stock']
    amount = float(request.form['amount'])
    time_horizon = int(request.form['time'])

    try:

        ticker = yf.Ticker(stock)
        data = ticker.history(period="1y")

        if data.empty:
            return f"Error: Could not fetch stock data for {stock}"

        # Daily returns
        data['returns'] = data['Close'].pct_change()
        returns = data['returns'].dropna()

        if returns.empty:
            return "Error: Not enough data."

        # Expected annual return
        expected_return = round(returns.mean() * 252 * 100, 2)

        # Annual volatility
        volatility = round(returns.std() * np.sqrt(252) * 100, 2)

        # Value at Risk (95%)
        VaR = round(np.percentile(returns, 5) * 100, 2)

        # Quantum risk probability
        risk = quantum_risk_analysis(returns.std())

        return render_template(
            "result.html",
            stock=stock,
            expected_return=expected_return,
            volatility=volatility,
            VaR=VaR,
            risk=risk
        )

    except Exception as e:
        return f"Error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)

