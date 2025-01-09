from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import whisper
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client.erp_assistant
requests_collection = db.requests

# NLP Model (Hugging Face Pipeline for NER)
nlp_model = pipeline("fill-mask", model="bert-base-uncased")

# STT Model (Whisper)
stt_model = whisper.load_model("base")

# Define API Models
class UserRequest(BaseModel):
    text: str

# Utility Function: Extract entities
import re

def extract_entities(text):
    """
    Extract entities dynamically from input text using regex.
    """
    # Default empty fields
    entities = {"project_number": None, "amount": None, "reason": None}

    # Extract project number (e.g., "project 123")
    project_match = re.search(r"project\s+(\d+)", text, re.IGNORECASE)
    if project_match:
        entities["project_number"] = project_match.group(1)

    # Extract amount (e.g., "300 riyals")
    amount_match = re.search(r"amount\s+is\s+(\d+)\s*(riyals|usd|dollars)?", text, re.IGNORECASE)
    if amount_match:
        entities["amount"] = amount_match.group(1) or amount_match.group(2)

    # Extract reason (e.g., "purchase laptops")
    reason_match = re.search(
        r"(?:to|for)\s+(?!request|project|money)(.+?)(?:\.\s|$)", text, re.IGNORECASE
    )
    if reason_match:
        entities["reason"] = reason_match.group(1).strip()

    return entities

@app.post("/process-voice-command/")
async def process_voice_command(request: UserRequest):
    try:
        text = request.text

        # Extract entities dynamically from input text
        entities = extract_entities(text)

        # Check if any required field is missing
        if not entities["project_number"] or not entities["amount"] or not entities["reason"]:
            raise HTTPException(
                status_code=500,
                detail="Missing required fields: project_number, amount, or reason."
            )

        # Save to MongoDB if all fields are present
        new_request = {
            "project_number": entities["project_number"],
            "amount": int(entities["amount"]),
            "reason": entities["reason"]
        }
        result = requests_collection.insert_one(new_request)

        return {
            "message": "Request successfully processed and saved!",
            "request_id": str(result.inserted_id),
            "entities": entities
        }
    except HTTPException as e:
        # Reraise HTTPException with 500 status if missing fields
        raise e
    except Exception as e:
        # General exception handling
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve all saved requests
@app.get("/requests/")
async def get_all_requests():
    try:
        requests = list(requests_collection.find())
        for request in requests:
            request["_id"] = str(request["_id"])  # Convert ObjectId to string for JSON serialization
        return {"requests": requests}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
