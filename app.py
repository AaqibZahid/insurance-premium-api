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

# Data exploration
"""
Fields in the raw dataset
    - age
    - weight
    - height
    - income_lpa
    - smoker
    - city
    - occupation
    - insurance_premium_category (target)
"""

# FASTAPI app
from fastapi import FastAPI, Query, Path
app = FastAPI()

# define the Pydantic data model class for validations
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, List, Annotated

class InsuranceModel(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the person")]
    weight: Annotated[float, Field(..., gt=0, description="weight in kilograms" )]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="height in meters")]
    income_lpa: Annotated[float, Field(..., gt=0, description="annual income in normalized numeric representation")]
    smoker: Annotated[bool, Field(..., description="is the person a habitual smoker or not")]
    city: Annotated[str, Field(..., description="city that the person is from")]
    occupation: Annotated[Literal[ 'retired','freelancer','student','government_job', 'business_owner','unemployed' 'private_job'] , Field(..., description="job domain of the person among 'retired','freelancer','student','government_job', 'business_owner','unemployed', or 'private_job'")]

# field validator for auto-title-casing the city parameter value
    @field_validator('city')
    @classmethod
    def validateCity(cls, v:str) -> str:
        return v.strip().title()


# computed fields (of the transformed dataset) using the existing raw dataset fields
    @computed_field
    @property
    def bmi(self) -> float:
        return round (self.weight / (self.height ** 2),2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def city_tier(city) -> int:
        tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
        tier_2_cities = [
            "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
            "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
            "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
            "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
            "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
            "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
        ]
        if city in tier_1_cities:
            return 1
        elif city in tier_2_cities:
            return 2
        else:
            return 3

# writing the POST endpoint function

import pandas as pd
from fastapi.responses import JSONResponse

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