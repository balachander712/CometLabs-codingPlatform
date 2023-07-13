from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse

from app.api.admin.schemas import Question, Solution
from app.core.database import get_database_connection
from app.core.security import security, validate_roles
from app.utils.sphere.create_problem import SphereAPI

router = FastAPI()



@router.post("/questions/check-solution")
async def check_solution(solution: Solution):
    client = get_database_connection()
    sphere_api = SphereAPI()
    db = client["CometLabs"]
    collection = db["questions"]  # Replace with your collection name
    question = collection.find_one({"question_id": int(solution.question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    collection = db["test_cases"]
    test_cases = collection.find({"question_id": question["question_id"]})
    test_cases = [
        {**test_case, "test_case_id": str(test_case["_id"]), "_id": None}
        for test_case in test_cases
    ]
    result = sphere_api.validate_result(solution.solution, test_cases)
    if result == "accepted":
        return JSONResponse(
            status_code=200,
            content="Problem Submission Successful"
        )
    else:
        return JSONResponse(
            status_code=200,
            content="Problem Submission UnSuccessful"
        )
