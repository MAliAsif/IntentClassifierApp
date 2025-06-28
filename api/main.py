from fastapi import FastAPI, status , HTTPException , Body , Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field , field_validator , validator
from fastapi.testclient import TestClient

import pickle
import numpy as np
import pandas as pd
import re

from api.models import PostSchema, UserSchema, UserLoginSchema
from Auth.jwt_handler import signJWT  # Import from the auth folder
from Auth.jwt_bearer import JWTBearer  

from api.endpoints import router  # Import the router from endpoints.py
import httpx

app = FastAPI()


# Model loading on startup with caching
@app.on_event("startup")
def load_model():
    global model, cv, encoder
    try:
        # Load the ML model, CountVectorizer, and LabelEncoder at startup
        with open('ml/model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('ml/cv.pkl', 'rb') as f:
            cv = pickle.load(f)
        with open('ml/encoder.pkl', 'rb') as f:
            encoder = pickle.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")


# Include the API routes from endpoints.py
app.include_router(router)
