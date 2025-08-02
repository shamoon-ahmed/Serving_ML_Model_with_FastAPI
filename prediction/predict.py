import pickle

with open('model_training/model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_acne(data: dict):

    {
        'age': data.age,
        'gender': data.gender,
        'weight_kg': data.weight_kg,
        'diet': data.diet,
        'sleep_hours': data.sleep_hours,
        'water_intake_liters': data.water_intake_liters,
        'smoking_or_vaping': data.smoking_or_vaping
        }
    
    prediction = model.predict(data)[0]

    return prediction