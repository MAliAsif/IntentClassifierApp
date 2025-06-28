from pydantic import BaseModel, Field

class ClassificationResponse(BaseModel):
    intent: str = Field(
        ...,
        description="The predicted intent category (e.g., email, calendar_schedule, web_search, knowledge_query)",
        example="web_search"
    )
    confidence: float = Field(
        ...,
        description="Model's confidence score for the predicted intent",
        example=0.92
    )

    