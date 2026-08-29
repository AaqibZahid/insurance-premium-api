import pickle
import pandas as pd
from pathlib import Path

# get the pickle file in the code (absolute path so it works from any working directory)
MODEL_PATH = Path(__file__).parent / "model.pkl"
with open(MODEL_PATH, 'rb') as file:
    model = pickle.load(file)

# ML flow's model registery traacks what version of the model we have but here we set this up manually
MODEL_VERSION = "1.0.0"

class_labels = model.classes_.tolist()

def predictOutput(user_input: dict):

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)
    
    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }
