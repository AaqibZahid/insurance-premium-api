from fastapi import FastAPI, Query, Path
from fastapi.responses import JSONResponse
from schema.user_input import InsuranceModel 
from model.predict import predictOutput, model, MODEL_VERSION
from schema.prediction_response import PredictionResponse

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
@app.post('/predict', response_model=PredictionResponse)
def predict(data: InsuranceModel):
    user_input = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }

    try:
        pred = predictOutput(user_input)

        #you can also use:
        # user_input_dict = pd.DataFrame([data.model_dump(exclude=["age", "height", "weight", "smoker", "city"])])
        return JSONResponse(
            status_code=200,
            content=pred
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})