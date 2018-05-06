import json
import requests
from firebase import firebase
from flask import Flask
from flask import request
from flask import render_template
import pyrebase
import serial
from time import sleep

config = {
  "apiKey": "AIzaSyAt3SehcP9qPDvLTgrCXeWmwWo15MzBTqA",
  "authDomain": "prediction-bd050.firebaseapp.com",
  "databaseURL": "https://prediction-bd050.firebaseio.com",
  "storageBucket": "prediction-bd050.appspot.com",
  "serviceAccount": "/Users/yz/Documents/GitHub/disobedient-electronics/prediction-0308f7f153ab.json"
}
firebase = pyrebase.initialize_app(config)

# authenticate a user
# authUser = firebase.auth()
user = firebase.auth().sign_in_with_email_and_password("youchunyz@gmail.com", "eadesigner")
db = firebase.database()

app = Flask(__name__)

# enable later
ser = serial.Serial('/dev/tty.usbmodem14111', 9600)

def auth(customer_id, api_key):
    try:
        credentials = {
            'customer_id': 3638,
            'api_key': 'sgi70ghc2dm27lbnvk8psjfnbf'
        }
        response = requests.post('https://api.applymagicsauce.com/auth', json=credentials)
        response.raise_for_status()
        return response.json()['token']
    except requests.exceptions.HTTPError as e:
        print e.response.json()

def predict_from_text(token, text):
    try:
        response = requests.post(url='https://api.applymagicsauce.com/text',
                                 params={
                                     'source': 'STATUS_UPDATE',
                                     'traits': 'BIG5_Neuroticism,BIG5_Agreeableness,BIG5_Openness,BIG5_Extraversion,BIG5_Conscientiousness'
                                },
                                 data=text,
                                 headers={'X-Auth-Token': token})
        response.raise_for_status()
        print (response.url)
        return response.json()
    except requests.exceptions.HTTPError as e:
        print e.response.json()

# auth
token = auth(3638, 'sgi70ghc2dm27lbnvk8psjfnbf')

# start the app
@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

    prediction_result = predict_from_text(token, text)
    print json.dumps(prediction_result, indent=4)
    db.set(prediction_result, user['idToken'])

    # enable later
    # get the value from response
    print "Sending serial data"
    value = []
    for index in range(0,5):
        temp = prediction_result['predictions'][index]['trait']
        output = prediction_result['predictions'][index]['value']
        if temp == 'BIG5_Agreeableness':
            value.insert(0, output)
        else:
            if temp == 'BIG5_Neuroticism':
                value.insert(1, output)
            else: 
                if temp == 'BIG5_Openness':
                   value.insert(2, output)
                else:
                    if temp == 'BIG5_Conscientiousness':
                        value.insert(3, output)
                    else:
                        if temp == 'BIG5_Extraversion':
                            value.insert(4, output)

    for index in range(0,5):
        # send the value through serial
        ser.write(chr(int(value[index]*127)))
        print (int(value[index]*127)*4+240)
        # print ser.readline()

    return render_template("index.html")

if __name__ == '__main__':
    app.run()
    