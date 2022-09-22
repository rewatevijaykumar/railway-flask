import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from pickle import dump
from pickle import load
import json
import os

app = Flask(__name__)

# Reading the data
data=pd.read_csv("Gold_data.csv")
data['date'] = pd.to_datetime(data['date'])
data.set_index('date',inplace=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        print(request.form.get('days'))
        try:
            days = int(request.form['days'])
                        
            # Loading the model we already created
            model=load(open('hwf.sav','rb'))
            predictions=model.forecast(days)
            pred_df=pd.DataFrame({"Prediction":predictions})
            pred_df.insert(loc=0, column='Date', value=pred_df.index.strftime('%d/%m/%Y'))
            pred_df = pred_df.round(2)
            pred_df = pred_df.reset_index(drop=True)
            pred_df.index = np.arange(1, len(pred_df) + 1)
            json_records = pred_df.reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
        except ValueError:
            return render_template('home.html',error = "Please enter valid values")
    return render_template('home.html',
    column_names=['Number of Day','Date','Price'], 
    data=data,
    legend = f'Gold Forecast for {days} days',
    labels=list(pred_df['Date'].values.tolist()), 
    values = list(pred_df['Prediction'].values.tolist()))
    
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
