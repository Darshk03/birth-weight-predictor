from flask import Flask , jsonify , render_template , request
import pandas as pd
import pickle

app = Flask(__name__)

@app.route('/',methods = ["GET"])
def home():
    return render_template("index.html")

def get_cleaned_data(form_data):
    gestation = form_data['gestation']
    parity = form_data['parity']
    age = form_data['age']
    height = form_data['height']
    weight = form_data['weight']
    smoke = form_data['smoke']
    
    cleaned_data = {
        'gestation': float(gestation),
        'parity': int(parity),
        'age': int(age),
        'height': float(height),
        'weight': float(weight),
        'smoke': int(smoke)
    }
    
    return cleaned_data

## define your endpoint

@app.route('/predict' , methods = ['POST'])
def get_prediction():
    
    # get data from user
    baby_data_form = request.form

    baba_data_cleaned =  get_cleaned_data(baby_data_form)
    
    #convert into dataframe
    baby_df = pd.DataFrame([baba_data_cleaned])
    
    #load ml trained model
    with open('model/model.pkl','rb') as obj:
        model = pickle.load(obj)
        
    # make a predictions on new/user/unseen data
    predictions = model.predict(baby_df)

    #prediction is in numpy array
    predictions = round(float(predictions),2)
    
    # Ensure prediction is not negative
    if predictions < 0:
        predictions = 0.0
    
    return render_template("index.html",predictions = predictions)
    
if __name__ == "__main__":
    app.run(debug=True)