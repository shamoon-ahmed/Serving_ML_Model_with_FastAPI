from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from prediction.predict import predict_acne
import pandas as pd

app = FastAPI()

@app.post('/predict')
def predict_acne_risk(data: UserInput):
    input_df = pd.DataFrame([{
        'age': data.age,
        'gender': data.gender,
        'weight_kg': data.weight_kg,
        'diet': data.diet,
        'sleep_hours': data.sleep_hours,
        'water_intake_liters': data.water_intake_liters,
        'smoking_or_vaping': data.smoking_or_vaping
        }])
    
    try:
        prediction = predict_acne(input_df)

        risk = 'acne risk' if prediction == 1 else 'no acne risk'

        return JSONResponse(status_code=201, content={'message':f"You have {risk}."})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={'Error': str(e)})