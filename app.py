import pickle
from fastapi import FastAPI, Query, Path
import pandas as pd
from fastapi.responses import JSONResponse
from schema.user_input import InsuranceModel 

# get the pickle file in the code
with open("model/model.pkl", 'rb') as file:
    model = pickle.load(file)

# ML flow's model registery traacks what version of the model we have but here we set this up manually
MODEL_VERSION = "1.0.0"

# FASTAPI app
app = FastAPI()

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