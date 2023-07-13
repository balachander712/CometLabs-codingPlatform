from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.api.admin.schemas import Question
from app.core.database import get_database_connection
from app.core.security import security, validate_roles

router = FastAPI()


@router.post("/admin/questions/add")
async def add_question(credentials: HTTPAuthorizationCredentials = Depends(security), question: Question = None):
    await validate_roles(credentials)
    client = get_database_connection()
    db = client["CometLabs"]  # Replace "CometLabs" with your actual database name
    collection = db["questions"] # Replace with your collection name
    existing_question = collection.find_one({"question_id": question.question_id})
    if existing_question:
        raise HTTPException(status_code=400, detail="Question ID already exists")
    collection.insert_one(question.dict())
    return {"message": "Question added successfully"}