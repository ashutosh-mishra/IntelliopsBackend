import unittest
import requests
import uuid

class TestAPI(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'  # replace with your API base URL

    def test_workflow(self):
        # Test create user
        user_id = str(uuid.uuid4())
        user_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "id": user_id
        }
        response = requests.post(f'{self.BASE_URL}/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), user_data)

        # Test get user
        response = requests.get(f'{self.BASE_URL}/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), user_data)

        # Test create company
        company_id = str(uuid.uuid4())
        company_data = {
            "name": "Acme Corp",
            "userId": user_id,
            "id": company_id
        }
        response = requests.post(f'{self.BASE_URL}/companies', json=company_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), company_data)

        # Test get company
        response = requests.get(f'{self.BASE_URL}/companies/{company_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), company_data)


if __name__ == '__main__':
    unittest.main()