# Insurance Premium Predictor

A small FastAPI service that predicts an insurance premium category (Low / Medium / High) from a person's basic details like age, weight, height, income, whether they smoke, their city, and their occupation.

## Project structure

- `app.py` — the FastAPI app with the endpoints
- `schema/` — request and response models
- `config/` — city tier lists used to classify cities
- `model/` — the trained model (`model.pkl`) and the prediction logic
- `Dockerfile` + `.dockerignore` — for building a container image
- `.github/workflows/` — CI that builds the image and smoke-tests the API

## Endpoints

| Method | Path      | Description                                 |
|--------|-----------|---------------------------------------------|
| GET    | `/`       | Tells you the API is running                |
| GET    | `/health` | Health check plus model version and status  |
| POST   | `/predict`| Takes the details and returns a prediction  |

Example `POST /predict` body:

```json
{
  "age": 34,
  "weight": 70.0,
  "height": 1.7,
  "income_lpa": 12.5,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

Response:

```json
{
  "predicted_category": "Low",
  "confidence": 0.79,
  "class_probabilities": {
    "High": 0.01,
    "Low": 0.79,
    "Medium": 0.2
  }
}
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

The API is then available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## Run with Docker

```bash
docker build -t insurance-premium-predictor:1.0.0 .
docker run -p 8000:8000 insurance-premium-predictor:1.0.0
```

## Notes

Docker basics and how the pieces fit together are covered in [this gist](https://gist.github.com/AaqibZahid/df4dcf13330d4f62ba49d2080011a373).
