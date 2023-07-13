from fastapi import FastAPI
from app.api.auth.sign_up import router as signup_router
from app.api.auth.login import router as login_router
from app.api.admin.routers.add_question import router as add_question
from app.api.admin.routers.delete_question import router as delete_question
from app.api.admin.routers.edit_question import router as edit_question
from app.api.admin.routers.add_test_case import router as add_test_case
from app.api.users.check_solution import router as check_solution

app = FastAPI()

app.include_router(signup_router)
app.include_router(login_router)
app.include_router(add_question.router)
app.include_router(delete_question.router)
app.include_router(edit_question.router)
app.include_router(add_test_case.router)
app.include_router(check_solution.router)

