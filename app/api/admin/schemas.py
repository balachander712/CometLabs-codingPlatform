from pydantic import BaseModel


class Question(BaseModel):
    question_id: int
    question_name: str
    question_text: str

# Model for Test Case
class TestCase(BaseModel):
    question_id: int
    test_case_id: int
    input_data: str
    expected_output: str

# Model for Solution
class Solution(BaseModel):
    question_id: int
    solution: str