from fastapi import FastAPI, status , HTTPException , Body , Depends , APIRouter

from fastapi.responses import JSONResponse
from fastapi import HTTPException
from api.models import PostSchema, UserSchema, UserLoginSchema
from Auth.jwt_handler import signJWT
from Auth.jwt_bearer import JWTBearer
import pickle
import numpy as np
import pandas as pd
import re

from api.models import UserInput,UserInputBatch
from pydantic import BaseModel, Field, computed_field , field_validator , validator
from ml.model_loader import load_models, model, cv, encoder  # Import the models and load_models function
from response_models.classification_response import ClassificationResponse
# from response_models.batch_classification_response import BatchClassificationResponse  # Import the response model
from response_models.batch_classification_response import BatchClassificationResponse  # Import the batch response model

# Now you can use `model`, `cv`, and `encoder` in your endpoints, as they are globally accessible.


# Create the APIRouter instance
router = APIRouter()

# Load the models manually when the app starts
model, cv, encoder = load_models()  # Unpack the models returned by load_models()


 

@router.get("/")
def hello():
    return {"message": "FastAPI is working!"}



# Health check endpoint
@router.get("/api/health")
def health_check():
    try:
        return {"status": "Healthy", "message": "API is up and running!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Model information endpoint
@router.get("/api/model/info")
def get_model_info():
    try:
        model_info = {
            "model_name": "Random Forest",
            "best_cross_validation_score": "96.13%",
            "training_accuracy": "100%",
            "testing_accuracy": "97.5%",
            "classification_report": {
                "overall_accuracy": "97%",
                "class_0 calender_schedule": "Precision: 1.00, Recall: 0.96, F1-Score: 0.98",
                "class_1 email_send": "Precision: 0.96, Recall: 1.00, F1-Score: 0.98",
                "class_2 general_chat": "Precision: 1.00, Recall: 0.96, F1-Score: 0.98",
                "class_3 knowledge_query": "Precision: 1.00, Recall: 0.96, F1-Score: 0.98",
                "class_4 web_search": "Precision: 0.93, Recall: 1.00, F1-Score: 0.96"
            },
            "averages": {
                "macro_avg": "Precision: 0.98, Recall: 0.97, F1-Score: 0.98",
                "weighted_avg": "Precision: 0.98, Recall: 0.97, F1-Score: 0.98"
            }
        }
        return model_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving model info: {str(e)}")




# Prediction endpoint, with JWT bearer clas dependency added
@router.post("/api/classify" , dependencies=[Depends(JWTBearer())] , response_model=ClassificationResponse)
async def classify_intent(user_input: UserInput):

    try:

        # Preprocess and vectorize the user input
        user_text = user_input.text.lower()  # Apply lowercase (if done during training)
        user_input_vector = cv.transform([user_text]).toarray()  # Vectorize the input

        # Predict the intent using the trained model
        predicted_class = model.predict(user_input_vector)

        # Decode the predicted class to get the original intent label
        predicted_intent = encoder.inverse_transform(predicted_class)

        predicted_prob = model.predict_proba(user_input_vector)  # Get probabilities for each class

        # Get the confidence (probability of the predicted class)
        confidence = np.max(predicted_prob)  # Confidence is the max probability of predicted class

        # Return the predicted intent as a JSON response in the required format
      # return JSONResponse(status_code=200, content={ "intent": predicted_intent[0] , "confidence": float(confidence)})
        
        # Return the predicted intent and confidence as a JSON response using the ClassificationResponse model
        return ClassificationResponse(
            intent=predicted_intent[0],  # Predicted intent
            confidence=float(confidence)  # Confidence score
        )
        

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the request: {str(e)}")



# Prediction endpoint for batch classification
@router.post("/api/classify/batch"  , dependencies=[Depends(JWTBearer())] , response_model=BatchClassificationResponse )
async def classify_batch(user_input: UserInputBatch):
    results = []
    try:
        # Process each query in the batch
        for idx, query in enumerate(user_input.texts, 1):  # Adding index starting from 1
            # Preprocess and vectorize the query
            query_text = query.lower()
            query_vector = cv.transform([query_text]).toarray()

            # Predict the intent and confidence using the trained model
            predicted_class = model.predict(query_vector)
            predicted_prob = model.predict_proba(query_vector)  # Get probabilities for each class

            # Decode the predicted class to get the original intent label
            predicted_intent = encoder.inverse_transform(predicted_class)[0]

            # Get the confidence (probability of the predicted class)
            confidence = np.max(predicted_prob)  # Confidence is the max probability of predicted class

            # Append the result to the list with the query number
            results.append({
                "query": f"query{idx}",  # Adding the query number as "query1", "query2", etc.
                "intent": predicted_intent,
                "confidence": float(confidence)
            })

        # Return the results as a JSON response
        # return JSONResponse(status_code=200, content=results)
                # Return the batch results
        return BatchClassificationResponse(results=results)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing batch request: {str(e)}")



# ● GET /api/model/info
# - Return model metadata and performance metrics
# ● GET /api/health




# In-memory user list (replace with a DB in a real app)
users = []


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@router.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    # Check if the email already exists in the users list
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="Error, user already exists")
    
    # Store the user without password hashing for now
    users.append(user.dict())  # Convert UserSchema to dict and append it (plain password)
    
    # Return the JWT token
    return signJWT(user.email)


@router.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    # Check if the email and password match any user
    matching_user = next((u for u in users if u["email"] == user.email and u["password"] == user.password), None)
    
    if matching_user:
        return signJWT(user.email)
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")




