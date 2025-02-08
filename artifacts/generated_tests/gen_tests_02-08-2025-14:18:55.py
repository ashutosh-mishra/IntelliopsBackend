import requests
import unittest
import uuid


class TestAPI(unittest.TestCase):
    base_url = "http://localhost:8000"

    def test_workflow(self):
        # Test Create User
        user_id = str(uuid.uuid4())
        response = requests.post(f"{self.base_url}/users", json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "id": user_id
        })
        self.assertEqual(response.status_code, 201)

        # Test Get User
        response = requests.get(f"{self.base_url}/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": user_id,
            "name": "John Doe",
            "email": "john.doe@example.com"
        })

        # Test Create Company
        company_id = str(uuid.uuid4())
        response = requests.post(f"{self.base_url}/companies", json={
            "name": "Acme Corp",
            "userId": user_id,
            "id": company_id
        })
        self.assertEqual(response.status_code, 201)

        # Test Get Company
        response = requests.get(f"{self.base_url}/companies/{company_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": company_id,
            "name": "Acme Corp",
            "userId": user_id
        })


if __name__ == "__main__":
    unittest.main()