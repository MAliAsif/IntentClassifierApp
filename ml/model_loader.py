import pickle
from fastapi import HTTPException
import os 

# Global variables to hold the model, cv, and encoder
model = None
cv = None
encoder = None

def load_models():
    try:
        current_dir = os.path.dirname(__file__)

        # Load the ML model, CountVectorizer, and LabelEncoder at startup
        with open(os.path.join(current_dir, 'model.pkl'), 'rb') as f:
            model = pickle.load(f)
        with open(os.path.join(current_dir, 'cv.pkl'), 'rb') as f:
            cv = pickle.load(f)
        with open(os.path.join(current_dir, 'encoder.pkl'), 'rb') as f:
            encoder = pickle.load(f)
        # Return the loaded models
        return model, cv, encoder

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")