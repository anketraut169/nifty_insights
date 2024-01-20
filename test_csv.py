from flask import Flask, request
import pandas as pd
import numpy as np

app = Flask(__name__)


def daily_volatility(data):
    data['Daily Returns'] = (data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1)
    dailyVolatility = data['Daily Returns'].std()
    return dailyVolatility

def annualized_volatility(DailyVolatility,len_data):
    annualizedVolatility = DailyVolatility * np.sqrt(len_data) 
    return annualizedVolatility

@app.route('/volatility', methods=['POST'])
def volatility(): 
    """
    Parameters: file (file)  CSV file 
    """  
    try:
        if 'file' in request.files:
            file = request.files['file']
            data = pd.read_csv(file)

        data.rename(columns=lambda x: x.strip(), inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date')

        len_data = len(data)
        DailyVolatility =  daily_volatility(data)
        Annualizedvolatility =  annualized_volatility(DailyVolatility,len_data)

        result = {
            "daily_volatility": DailyVolatility,
            "annualized_volatility": Annualizedvolatility
        }

        return result

    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(debug=True)
