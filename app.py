"""
- This file contains code for processing of the user input data for the POST method API of the model for its inference.
- it contains:
    - the import model pickle file
    - the POST api endpoint with the query params
    - the data model for type and processing validation of the input data
    - the processing of user request and then the response for it (prediction) at localhost 
"""

# get the pickle file in the code
import pickle
with open("model/model.pkl", 'rb') as file:
    model = pickle.load(file)

# ML flow's model registery traacks what version of the model we have but here we set this up manually
MODEL_VERSION = "1.0.0"

# FASTAPI app
from fastapi import FastAPI, Query, Path
app = FastAPI()

import pandas as pd
from fastapi.responses import JSONResponse
from schema.user_input import InsuranceModel 

# Home endpoint for telling that the api is running and whats it about (human readable)
@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API"}

# Health check endpoint - forced & recommended to set this up by management services like Kubernetes/ elastic load balancer. They hit at this endpoint to check health of api
@app.get("/health")
def healthCheck():
    return {
        "status": "OK",
        "version": MODEL_VERSION,
        "model_loaded": model is not None
    }

# writing the POST endpoint function
@app.post('/predict')
def predict(data: InsuranceModel):
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

    #you can also use:
    # user_input_dict = pd.DataFrame([data.model_dump(exclude=["age", "height", "weight", "smoker", "city"])])

    pred = model.predict(input_df)[0]
    
    probs = model.predict_proba(input_df)[0]
    classes = model.classes_

    class_probabilities = {
        cls: float(prob)
        for cls, prob in zip(classes, probs)
    }

    confidence = float(max(probs))

    return JSONResponse(
        status_code=200,
        content={
            "response": {
                "predicted_category": pred,
                "confidence": confidence,
                "class_probabilities": class_probabilities
            }
        }
    )