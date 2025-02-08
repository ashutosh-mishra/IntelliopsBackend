import unittest
import requests
import json

class TestAPI(unittest.TestCase):
    BASE_URL = 'http://localhost:5000' # change with your actual API base URL

    def test_workflow(self):
        # Test: Create a user
        response = requests.post(f'{self.BASE_URL}/users', json={
            'name': 'John Doe', 
            'email': 'john.doe@example.com'
        })
        self.assertEqual(response.status_code, 201)
        user = response.json()
        self.assertEqual(user['name'], 'John Doe')
        self.assertEqual(user['email'], 'john.doe@example.com')

        # Test: Get the user
        response = requests.get(f'{self.BASE_URL}/users/{user["id"]}')
        self.assertEqual(response.status_code, 200)
        get_user = response.json()
        self.assertEqual(get_user, user)

        # Test: Create a company
        response = requests.post(f'{self.BASE_URL}/companies', json={
            'name': 'Acme Corp', 
            'userId': user['id']
        })
        self.assertEqual(response.status_code, 201)
        company = response.json()
        self.assertEqual(company['name'], 'Acme Corp')
        self.assertEqual(company['userId'], user['id'])

        # Test: Get the company
        response = requests.get(f'{self.BASE_URL}/companies/{company["id"]}')
        self.assertEqual(response.status_code, 200)
        get_company = response.json()
        self.assertEqual(get_company, company)


if __name__ == '__main__':
    unittest.main()