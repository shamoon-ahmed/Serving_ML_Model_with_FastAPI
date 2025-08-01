from pydantic import BaseModel, Field
from typing import Annotated, Literal
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

class UserInput(BaseModel):

    age : Annotated[int, Field(..., title='Age', description='Age of individual', gt=0, lt=130)]
    gender : Annotated[Literal['male', 'female'], Field(..., title='Gender', description='Gender of individual')]
    weight_kg : Annotated[float, Field(..., title='Weight', description='Weight of individual (in Kgs)', gt=0)]
    diet : Annotated[Literal['healthy', 'unhealthy'], Field(..., title='Diet', description='Diet that you take', examples=['healthy', 'unhealthy'])]
    sleep_hours : Annotated[float, Field(..., title='Sleep Hours', description='How many hours do you sleep?', gt=0)]
    water_intake_liters : Annotated[float, Field(..., title='Water Intake', description='Water Intake (in liters)')]
    smoking_or_vaping : Annotated[Literal['yes', 'no'], Field(..., title='Smoke or Vape', description='Do you smoke or vape?', examples=['yes', 'no'])]

@app.post('/predict')
def predict_acne_risk(data: UserInput):

    input_df = pd.DataFrame([
        {
        'age': data.age,
        'gender': data.gender,
        'weight_kg': data.weight_kg,
        'diet': data.diet,
        'sleep_hours': data.sleep_hours,
        'water_intake_liters': data.water_intake_liters,
        'smoking_or_vaping': data.smoking_or_vaping
        }
    ]
        )
    
    prediction = model.predict(input_df)[0]

    risk = 'acne_risk' if prediction == 1 else 'no acne risk'

    return JSONResponse(status_code=201, content={'message':f"You have {risk}"})