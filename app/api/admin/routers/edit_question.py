from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials

from api.admin.schemas import Question
from core.database import get_database_connection
from core.security import security, validate_roles

router = FastAPI()


@router.put("/admin/questions/edit")
async def edit_question(credentials: HTTPAuthorizationCredentials = Depends(security), question: Question = None):
    await validate_roles(credentials)
    client = get_database_connection()
    db = client["CometLabs"]
    collection = db["questions"]
    existing_question = collection.find_one({"question_id": question.question_id})
    if not existing_question:
        raise HTTPException(status_code=404, detail="Question not found")
    collection.replace_one({"question_id": question.question_id}, question.dict())
    return {"message": "Question updated successfully"}