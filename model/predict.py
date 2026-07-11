import pickle
import pandas as pd

# get the pickle file in the code
with open("model/model.pkl", 'rb') as file:
    model = pickle.load(file)

# ML flow's model registery traacks what version of the model we have but here we set this up manually
MODEL_VERSION = "1.0.0"

def predictOutput( user_input: dict ):
    input_df = pd.DataFrame([user_input])
    output = model.predict(input_df)[0]
    # probs = model.predict_proba(input_df)[0]
    # classes = model.classes_
    # class_probabilities = {
    #     cls: float(prob)
    #     for cls, prob in zip(classes, probs)
    # }
    # confidence = float(max(probs))

    return output
