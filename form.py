import json
import requests
from firebase import firebase
from flask import Flask
from flask import request
from flask import render_template
import pyrebase
import serial
from time import sleep

# prompt user in terminal to get input
# post = raw_input('Hey! What is happening? ')
# firebase = firebase.FirebaseApplication('https://prediction-bd050.firebaseio.com', None)
# result = firebase.post('/posts', post)

config = {
  "apiKey": "AIzaSyAt3SehcP9qPDvLTgrCXeWmwWo15MzBTqA",
  "authDomain": "prediction-bd050.firebaseapp.com",
  "databaseURL": "https://prediction-bd050.firebaseio.com",
  "storageBucket": "prediction-bd050.appspot.com",
  "serviceAccount": "/Users/yz/Documents/GitHub/disobedient-electronics/prediction-0308f7f153ab.json"
}
firebase = pyrebase.initialize_app(config)

# authenticate a user
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("youchunyz@gmail.com", "eadesigner")
db = firebase.database()

app = Flask(__name__)

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
                                     'source': 'OTHER'
                                 },
                                 data=text,
                                 headers={'X-Auth-Token': token})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print e.response.json()

# /auth
token = auth(3638, 'sgi70ghc2dm27lbnvk8psjfnbf')

# /start the app
@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    # result = firebase.post('/posts', text)

    prediction_result = predict_from_text(token, text)
    print json.dumps(prediction_result, indent=4)
    db.set(prediction_result, user['idToken'])
    # result = firebase.post('/predictions', prediction_result)

    ser = serial.Serial('/dev/tty.usbmodem14611', 9600)
    print ser 
    print "Sending serial data"
    print prediction_result

    # counter = 32
    # while True:
    #     counter +=1
    #     ser.write(counter)
    #     print ser.readline()
    #     sleep(.1)
    
    counter = 32
    while True:
        counter +=1
        ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
        print ser.readline() # Read the newest output from the Arduino
        sleep(.1) # Delay for one tenth of a second
        if counter == 255:
            counter = 32

    return text

if __name__ == '__main__':
    app.run()
