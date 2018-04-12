import json
import requests
from firebase import firebase
from flask import Flask
from flask import request
from flask import render_template

# post = raw_input('Hey! What is happening? ')
firebase = firebase.FirebaseApplication('https://prediction-bd050.firebaseio.com', None)
# result = firebase.post('/posts', post)

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
    result = firebase.post('/posts', text)

    prediction_result = predict_from_text(token, text)
    print json.dumps(prediction_result, indent=4)
    result = firebase.post('/predictions', prediction_result)

    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0')


# def predict_from_like_ids(token, like_ids):
#     try:
#         response = requests.post(url='https://api.applymagicsauce.com/like_ids',
#                                  json=like_ids,
#                                  headers={'X-Auth-Token': token})
#         response.raise_for_status()
#         if response.status_code == 204:
#             raise ValueError('Not enough predictive like ids provided to make a prediction')
#         else:
#             return response.json()
#     except requests.exceptions.HTTPError as e:
#         print e.response.json()
#     except ValueError as e:
#         print e


# # /like ids
# prediction_result = predict_from_like_ids(token, ["5845317146", "6460713406", "22404294985", "35312278675",
#                                                   "105930651606", "171605907303", "199592894970", "274598553922",
#                                                   "340368556015", "100270610030980"])
# print json.dumps(prediction_result, indent=4)
