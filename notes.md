# Serving ML Model with FastAPI
### Acne Risk Predictor

---------------------

In this repo, we're serving a Machine Learning Model, an Acne Risk Predictor that prdicts whether someone is likely to develop acne based on some features like age, diet, sleep hours, etc.

## Training Our Model

The very first step that we took is training our model on a ML algorithm and saving that file for later use in pickle or any other suitable format. 

- We imported a .csv file and trained our model on it. 
```powershell
df = pd.read_csv('acne_risk_dataset.csv')
```
- Saved that model pipeline in .pkl format for later use in frontend.
```powershell
import pickle

# Save the trained pipeline using pickle
pickle_model_path = "model.pkl"
with open(pickle_model_path, "wb") as f:
    pickle.dump(pipeline, f)
```

## Creating Pydantic Model

In a different file **schema/user_input.py** we built a Pydantic model for data and type validation of the features that we want the user to provide to get the right prediction (acne risk)

```powershell
class UserInput(BaseModel):
    
    age : Annotated[int, Field(..., title='Age', description='Age of individual', gt=0, lt=130)]
    gender : Annotated[Literal['male', 'female'], Field(..., title='Gender', description='Gender of individual')]
    weight_kg : Annotated[float, Field(..., title='Weight', description='Weight of individual (in Kgs)', gt=0)]
    diet : Annotated[Literal['healthy', 'unhealthy'], Field(..., title='Diet', description='Diet that you take', examples=['healthy', 'unhealthy'])]
    sleep_hours : Annotated[float, Field(..., title='Sleep Hours', description='How many hours do you sleep?', gt=0)]
    water_intake_liters : Annotated[float, Field(..., title='Water Intake', description='Water Intake (in liters)')]
    smoking_or_vaping : Annotated[Literal['yes', 'no'], Field(..., title='Smoke or Vape', description='Do you smoke or vape?', examples=['yes', 'no'])]
```

## Creating our endpoint

Then, in **app.py**<br>
- We created our endpoint **/predict** that takes the pydantic object as parameter
- Passed the features data as a Pandas Dataframe to our model that we imported earlier in the same file.
- Then in **prediction/predict.py** Called the predict function **model.predict(input_data)** that calls the Pipeline object in our **model** file

To understand this better, basically this happens: <br>
- This is our Pipeline object in the model.pkl file

```powershell
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(random_state=42))
])
```

- and this is what we call with **model.predict(input_data)[0]** where the **X_test** is actually **input_df**

```powershell
y_pred = pipeline.predict(X_test)
```

Take a look at this endpoint code:

```powershell
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

    risk = 'acne risk' if prediction == 1 else 'no acne risk'

    return JSONResponse(status_code=201, content={'message':f"You have {risk}."})
```

Once we have our trained model, our endpoint created, we move on to creating our frontend with Streamlit

## Creating Frontend with Streamlit

So we made a button called **Predict Acne Risk** that when pressed, it hits this URL with the required data in json

```powershell
URL = 'http://127.0.0.1:8000/predict'
```

This is the data that is passed with our url

```powershell
if st.button("Predict Acne Risk"):
    input_data = {
        "age": age,
        "gender": gender,
        "weight_kg": weight_kg,
        "diet": diet,
        "sleep_hours": sleep_hours,
        "water_intake_liters": water_intake_liters,
        "smoking_or_vaping": smoking_or_vaping
    }
```

We get the response from requests, and displays the prediction. Otherwise, we raise an exception

```powershell
    try:
        response = requests.post(URL, json=input_data)
        result = response.json()

        if response.status_code == 200 or response.status_code == 201:
            st.success(f"Acne Risk Precition: {result['message']}")

        else:
            st.error(f"API Error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error('Server Error!')
```

To use our frontend made with Streamlit, we run our FastAPI server first, then our streamlit server inorder to have our endpoint work

Run Streamlit server with:

```powershell
streamlit run filename.py
```

## Dockerize The Entire Application

An additional step we took is dockerizing our Application. <br> So till now we need to run our FastAPI server, then run our streamlit application. But by dockerizing our application (means putting everything like libraries, their versions, all codes n stuff into a box). 
<br> <br>
That box is called an image. So we built an image of our application with the help of Dockerfile that contains all the commands to build a Docker image. We then pushed that Docker image to DockerHub so we can pull it later and anyone looking for an Acne Risk Predictor made with FastAPI and Streamlit can pull our image and run a container on their machine. 
<br> <br>
Our application would run the same way on the other users' machine as it was running in our machine. This is the benefit of Docker
<br> <br>
For the other user, to run the same application that is running perfectly on our machine, we take these steps:

1. **Build** an image of our application. This includes debugging and removing all the errors that might come while running our application until it runs perfectly.
- `docker build -t shamoonai/acne_risk_predictor .`
2. **Push** that image to DockerHub where our account is logged in. (We must login from our local environment as well inorder to push that image from VS code to DockerHub).
- To Login: `docker login`
- To push image to DockerHub: `docker push <image name>` in our case `docker push shamoonai/acne_risk_predictor`
3. **Pull** that image from DockerHub
- `docker pull <image name on DockerHub>` in our case `docker pull shamoonai/acne_risk_predictor`
4. **Run** our image that we just pulled from DockerHub. 
- `docker run -p <image name>` 
<br> <br> In our case, we have a FastAPI server and a Streamlit server. So we need to run both servers by adding both ports in the command.
- `docker run -p 8501:8501 -p 8000:8000 shamoonai/acne_risk_predictor`
<br> *8501:8501 to run the Streamlit server and 8000:8000 to run the FastAPI server*