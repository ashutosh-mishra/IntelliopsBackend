import requests
import unittest
import uuid

class TestUserAPI(unittest.TestCase):

    BASE_URL = "http://localhost:5000" # Replace with your server URL

    def test_create_and_get_user(self):
        # Test creating a new user
        user_id = str(uuid.uuid4())
        user_payload = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        response = requests.post(f"{self.BASE_URL}/users", json=user_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': user_id, 'name': 'John Doe', 'email': 'john.doe@example.com'})

        # Test getting the user details
        response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': user_id, 'name': 'John Doe', 'email': 'john.doe@example.com'})

class TestCompanyAPI(unittest.TestCase):

    BASE_URL = "http://localhost:5000" # Replace with your server URL

    def test_create_and_get_company(self):
        # Test creating a new company
        user_id = str(uuid.uuid4())
        company_id = str(uuid.uuid4())
        company_payload = {'name': 'Acme Corp', 'userId': user_id}
        response = requests.post(f"{self.BASE_URL}/companies", json=company_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': company_id, 'name': 'Acme Corp', 'userId': user_id})

        # Test getting the company details
        response = requests.get(f"{self.BASE_URL}/companies/{company_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': company_id, 'name': 'Acme Corp', 'userId': user_id})

class TestWorkflowAPI(unittest.TestCase):

    BASE_URL = "http://localhost:5000" # Replace with your server URL

    def test_workflow(self):
        # Create a new user
        user_id = str(uuid.uuid4())
        user_payload = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        response = requests.post(f"{self.BASE_URL}/users", json=user_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': user_id, 'name': 'John Doe', 'email': 'john.doe@example.com'})

        # Create a new company with the newly created user
        company_id = str(uuid.uuid4())
        company_payload = {'name': 'Acme Corp', 'userId': user_id}
        response = requests.post(f"{self.BASE_URL}/companies", json=company_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'id': company_id, 'name': 'Acme Corp', 'userId': user_id})

        # Get the company details and verify the userId matches with the created user
        response = requests.get(f"{self.BASE_URL}/companies/{company_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': company_id, 'name': 'Acme Corp', 'userId': user_id})

if __name__ == '__main__':
    unittest.main()