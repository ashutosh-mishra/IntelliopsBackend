import requests
import unittest
import uuid

class TestAPI(unittest.TestCase):
    base_url = 'http://localhost:5000'

    def test_workflow(self):
        # Test Creating a User
        user_data = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        response = requests.post(f'{self.base_url}/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        user_id = response.json()['id']
        self.assertEqual(response.json(), {'id': user_id, 'name': 'John Doe', 'email': 'john.doe@example.com'})

        # Test Getting a User
        response = requests.get(f'{self.base_url}/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': user_id, 'name': 'John Doe', 'email': 'john.doe@example.com'})

        # Test Creating a Company with User ID
        company_data = {'name': 'Acme Corp', 'userId': user_id}
        response = requests.post(f'{self.base_url}/companies', json=company_data)
        self.assertEqual(response.status_code, 201)
        company_id = response.json()['id']
        self.assertEqual(response.json(), {'id': company_id, 'name': 'Acme Corp', 'userId': user_id})

        # Test Getting a Company
        response = requests.get(f'{self.base_url}/companies/{company_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': company_id, 'name': 'Acme Corp', 'userId': user_id})

if __name__ == '__main__':
    unittest.main()