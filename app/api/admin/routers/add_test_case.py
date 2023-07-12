from typing import List

from fastapi import FastAPI, Depends
from fastapi.security import HTTPAuthorizationCredentials

from api.admin.schemas import TestCase
from core.database import get_database_connection
from core.security import security, validate_roles

router = FastAPI()

@router.post("/admin/questions/test-cases/add")
async def add_test_case(credentials: HTTPAuthorizationCredentials = Depends(security), test_cases: List[TestCase]=None):
    await validate_roles(credentials)
    client = get_database_connection()
    db = client["CometLabs"]  # Replace "CometLabs" with your actual database name
    collection = db["test_cases"]  # Replace with your collection name
    test_case_data = [test_case.dict() for test_case in test_cases]
    collection.insert_many(test_case_data)
    return {"message": "Test cases added successfully"}