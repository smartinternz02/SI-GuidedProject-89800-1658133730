import flask
from flask import request, render_template,jsonify
import joblib
import json
import requests

API_KEY = "JZiNJsN85XvXF0opStoGmM-1nFqgg2v3xMbuT482fRr5"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

app = flask.Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'])
def sendHomePage():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predictPerformance():
    cylinders = float(request.form['cylinders'])
    displacement = float(request.form['displacement'])
    horsepower = float(request.form['horsepower'])
    weight = float(request.form['weight'])
    acceleration = float(request.form['acceleration'])
    modelyear = float(request.form['modelyear'])
    origin = float(request.form['origin'])

    X = [[cylinders,displacement,horsepower,
          weight,acceleration,modelyear,origin]]



    payload_scoring = {"input_data": [{"field": [['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration','modelyear','origin']],
                                       "values": X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7f81e07f-9c33-4b37-8358-62ae141e55ce/predictions?version=2022-08-20', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    

    
    print("Scoring response")
    print(response_scoring.json())
    pred = response_scoring.json()


    output = pred['predictions'][0]['values'][0][0]
    print(output)
    
    return render_template('predict.html', predict=output)


if __name__ == "__main__":
    app.run(debug=False)