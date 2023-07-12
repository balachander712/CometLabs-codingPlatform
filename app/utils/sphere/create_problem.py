import json
import time
from typing import List

from dotenv import load_dotenv
import os
import requests

load_dotenv()

SPHERE_API_KEY = os.getenv("SPHERE_API_KEY")
PROBLEMS_API_ENDPOINT = os.getenv("PROBLEMS_API_ENDPOINT")


class SphereAPI():
    def __init__(self):
        self.add_problem_url = f"https://{PROBLEMS_API_ENDPOINT}/api/v4/problems?access_token={SPHERE_API_KEY}"
        self.submissions_url = f"https://{PROBLEMS_API_ENDPOINT}/api/v4/submissions?access_token={SPHERE_API_KEY}"
        self.create_submission_url = f'https://{PROBLEMS_API_ENDPOINT}/api/v4/submissions?access_token={SPHERE_API_KEY}'

    def create_submission(self, source_code: str, input_data: List, compiler_id: int):
        data = {
            'compilerId': compiler_id,
            'source': source_code,
            'input': input_data
        }
        response = requests.post(self.create_submission_url, json=data)
        submission_id = response.json().get('id')
        return submission_id

    def _make_submission_call(self, submission_id: str):
        url = f'https://{PROBLEMS_API_ENDPOINT}/api/v4/submissions/{submission_id}?access_token={SPHERE_API_KEY}'
        params = {
            'withOutput': True
        }
        response = requests.get(url, params=params)
        response = response.json()
        return response

    def get_submission_result(self, submission_id: str):
        response = self._make_submission_call(submission_id)
        while response["executing"]:
            time.sleep(5)
            response = self._make_submission_call(submission_id)
        if not response["executing"]:
            return response["result"]["status"]["name"]

    def validate_result(self, source_code: str, test_cases: List):
        print(source_code)
        input = []
        for test_case in test_cases:
            print(test_case)
            input.append(
                {
                    'input': test_case.get('input_data'),
                    'output': test_case.get('expected_output')
                }
            )
        submission_id = self.create_submission(source_code, input, compiler_id=116)
        time.sleep(5)
        return self.get_submission_result(submission_id)
