import json
import requests
import unittest

class TestUserAPI(unittest.TestCase):

    BASE_URL = "http://localhost:8000"

    def test_workflow(self):
        # Test Create User
        response = requests.post(
            f"{self.BASE_URL}/users",
            data=json.dumps({"name": "John Doe", "email": "john.doe@example.com"}),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 201)

        user_id = response.json()["id"]

        # Test Get User
        response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], user_id)

        # Test Create Company
        response = requests.post(
            f"{self.BASE_URL}/companies",
            data=json.dumps({"name": "Acme Corp", "userId": user_id}),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 201)

        company_id = response.json()["id"]

        # Test Get Company
        response = requests.get(f"{self.BASE_URL}/companies/{company_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], company_id)
        self.assertEqual(response.json()["userId"], user_id)

if __name__ == "__main__":
    unittest.main()