from pydantic import BaseModel, Field
from typing import List
from .classification_response import ClassificationResponse  # Import ClassificationResponse

class BatchClassificationResponse(BaseModel):
    results: List[ClassificationResponse] = Field(
        ...,
        description="A list of predicted intents and confidence scores for each query in the batch",
        example=[
            {"intent": "web_search", "confidence": 0.92},
            {"intent": "email", "confidence": 0.85}
        ]
    )
