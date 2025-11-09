from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
import os
from sklearn.metrics import accuracy_score, confusion_matrix

app = FastAPI()

# Get the directory of the current script
backend_dir = os.path.dirname(__file__)
model_path = os.path.join(backend_dir, "model.pkl")
data_path = os.path.join(backend_dir, "newdata.csv")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
model_data = joblib.load(model_path)
# Extract the pipeline from the dictionary if it's a dict, otherwise use it directly
if isinstance(model_data, dict):
    pipeline = model_data.get('model', model_data)
else:
    pipeline = model_data

# Define the input data model - only the 4 required features
class UserInput(BaseModel):
    introversion_extraversion: int
    risk_taking: int
    club_top1: str
    weekly_hobby_hours: int

@app.get("/data-summary")
def data_summary():
    df = pd.read_csv(data_path)

    # Replace NaN with None for JSON compatibility
    df = df.replace({np.nan: None})

    # Binarize teamwork preference, handling potential None values
    df['preference'] = df['teamwork_preference'].apply(lambda x: 'Team' if x is not None and x >= 4 else 'Solo')

    preference_distribution = df['preference'].value_counts().to_dict()
    introversion_distribution = df['introversion_extraversion'].dropna().value_counts().to_dict()
    risk_taking_distribution = df['risk_taking'].dropna().value_counts().to_dict()
    recent_submissions = df.tail(5).to_dict(orient='records')

    # Calculate model accuracy and confusion matrix
    # Ensure we only use rows where the target is not null for a fair evaluation
    eval_df = df.dropna(subset=['teamwork_preference', "introversion_extraversion", "risk_taking", "weekly_hobby_hours", "club_top1"])
    X = eval_df[["introversion_extraversion", "risk_taking", "weekly_hobby_hours", "club_top1"]]
    y_true = eval_df['teamwork_preference'].apply(lambda x: 1 if x >= 4 else 0)

    if not X.empty:
        y_pred = pipeline.predict(X)
        accuracy = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred).tolist()
    else:
        accuracy = 0
        cm = [[0,0],[0,0]]


    return {
        "preference_distribution": preference_distribution,
        "introversion_distribution": introversion_distribution,
        "risk_taking_distribution": risk_taking_distribution,
        "recent_submissions": recent_submissions,
        "accuracy": accuracy,
        "confusion_matrix": cm
    }

@app.post("/predict")
def predict(data: UserInput):
    print(f"Received data: {data.dict()}")  # Debug log
    
    # Create a dataframe for prediction from the input data
    prediction_df = pd.DataFrame([data.dict()])

    # Make a prediction
    prediction = pipeline.predict(prediction_df)[0]
    prediction_proba = pipeline.predict_proba(prediction_df)[0]

    # Save the prediction to CSV
    try:
        # Read existing CSV to get all columns
        existing_df = pd.read_csv(data_path)
        
        # Create a new row with all columns initialized to NaN
        new_row = pd.DataFrame([{col: np.nan for col in existing_df.columns}])
        
        # Fill in the values we have
        new_row['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row['introversion_extraversion'] = data.introversion_extraversion
        new_row['risk_taking'] = data.risk_taking
        new_row['club_top1'] = data.club_top1
        new_row['weekly_hobby_hours'] = data.weekly_hobby_hours
        
        # Add the predicted teamwork preference (convert back to 1-5 scale)
        new_row['teamwork_preference'] = 5 if prediction == 1 else 1
        
        # Append to CSV
        new_row.to_csv(data_path, mode='a', header=False, index=False)
        print(f"Successfully saved data to CSV")  # Debug log
    except Exception as e:
        print(f"Error saving to CSV: {e}")

    # Return the prediction
    if prediction == 1:
        preference = "Team"
    else:
        preference = "Solo"

    return {
        "prediction": preference,
        "prediction_probability": {
            "Solo": float(prediction_proba[0]),
            "Team": float(prediction_proba[1])
        }
    }