from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from core.database import get_database_connection
from core.security import security, validate_admin_roles

router = FastAPI()

@router.delete("/admin/questions/delete/{question_id}")
async def delete_question(credentials: HTTPAuthorizationCredentials = Depends(security), question_id: int = None):
    await validate_admin_roles(credentials)
    client = get_database_connection()
    db = client["CometLabs"]  # Replace "CometLabs" with your actual database name
    collection = db["questions"]  # Replace with your collection name
    existing_question = collection.find_one({"question_id": question_id})
    if not existing_question:
        raise HTTPException(status_code=404, detail="Question not found")
    collection.delete_one({"question_id": question_id})
    return {"message": "Question deleted successfully"}
