from pydantic import BaseModel, Field, EmailStr, field_validator , validator
from typing import List



# Original UserInput class with empty check
class UserInput(BaseModel):
    text: str = Field(..., min_length=5, max_length=500, example="Search hotels.")

    # Validator to ensure there are letters in the text and not only numbers
    @validator('text')
    def validate_text(cls, v):
        # Check if the text is empty
        if not v:
            raise ValueError('The text field cannot be empty.')
        
        # Check if the text contains only numbers
        if v.isdigit():
            raise ValueError('User Query cannot be only numbers.')
        return v


    
# Define a Pydantic model for batch input (multiple queries)
class UserInputBatch(BaseModel):
    texts: List[str]  # List of queries for batch classification

    # Validator for each text in the batch
    @validator('texts')
    def validate_texts(cls, v):
        if not v:
            raise ValueError('The list of texts cannot be empty.')
        for text in v:
            # Check if any text in the list is just digits
            if text.isdigit():
                raise ValueError(f'Query "{text}" cannot contain only numbers.')
            # Optionally, you can add more checks like minimum or maximum length
            if len(text) < 5 or len(text) > 500:
                raise ValueError(f'Query "{text}" must be between 5 and 500 characters.')
        return v



class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }