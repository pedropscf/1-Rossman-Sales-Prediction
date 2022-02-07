import json
import requests
import pandas as pd
import os
from flask import Flask, request, Response

# constants
token = '2021983632:AAFrd62jLcFWYVzwp1OyOCc2Zb1wUalqyO0'
data_path = '' #'/home/pedro/Documentos/repositories/1-Rossman-Sales-Prediction/'
# info about the bot
#https://api.telegram.org/bot2021983632:AAFrd62jLcFWYVzwp1OyOCc2Zb1wUalqyO0/getMe

# Get updates
#https://api.telegram.org/bot2021983632:AAFrd62jLcFWYVzwp1OyOCc2Zb1wUalqyO0/getUpdates

# Set webhook
#https://api.telegram.org/bot2021983632:AAFrd62jLcFWYVzwp1OyOCc2Zb1wUalqyO0/setWebhook?url=https://rossman-sales-prediction-bot.herokuapp.com/

# Send message
#https://api.telegram.org/bot2021983632:AAFrd62jLcFWYVzwp1OyOCc2Zb1wUalqyO0/sendMessage?chat_id=771524750&text=Hi, Pedro! I am the Rossman sales prediction bot. How can I help you?

def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot{}/'.format(token)
    url = url + 'sendMessage?chat_id={}'.format(chat_id)

    r = requests.post(url, json={'text':text} )
    print( 'Status code: {}'.format(r.status_code))

    return None

def parse_message(message):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']

    store_id = store_id.replace('/', '')

    try:
        store_id = int(store_id)
    
    except ValueError:
        store_id = 'error'

    return chat_id, store_id

def load_dataset(store_id):
    test_path = 'data/test.csv'
    store_path = 'data/store.csv'
    df10 = pd.read_csv(test_path, low_memory=False)
    df_store_raw = pd.read_csv(store_path, low_memory=False)
    # Merging test dataset + store
    df_test = pd.merge(df10, df_store_raw, how='left', on='Store')

    # Choose store for prediction
    df_test = df_test[df_test['Store'] == store_id]

    if not df_test.empty:
        # Remove close days
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop('Id', axis=1)

        # Convert test dataframe in json
        data = json.dumps(df_test.to_dict(orient='records'))

    else:
        data = 'error'

    return data

def predict_sales(data):
    # API Call
    url = 'https://rossman-sales-prediction-model.herokuapp.com/rossman/predict'
    header = {'Content-type': 'application/json'}
    #data = data

    r = requests.post(url, data=data, headers=header)
    print('Status Code {}'.format(r.status_code))

    d1 = pd.DataFrame(r.json(), columns=r.json()[0].keys())

    return d1

# API initialize
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        message = request.get_json()

        chat_id, store_id = parse_message(message)

        if store_id != 'error':
            #loading data
            data = load_dataset(store_id)

            if data != 'error':
                #prediction
                d1 = predict_sales(data)
                #calculation
                d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()
                    
                message = 'Store number {} will sell ${:,.2f} in the next 6 weeks'.format(d2['store'].values[0], d2['prediction'].values[0])

                #send message
                send_message(chat_id, message)
                return Response('Ok', status=200)
            else:
                send_message(chat_id, 'Store not available. Try another number')
                return Response('Ok', status=200)                

        else:
            send_message(chat_id, 'Insert the Store ID to predict sales of a Rossmann Store for the next 6 weeks. You can enter the ID by sending /Store_id or just the Store ID number.')
            return Response('Ok', status=200)

    else:
        return '<h1> Hi, I am the Rossman sales prediction bot, insert the Store ID to predict sales for the next 6 weeks. <h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port, debug=True)
