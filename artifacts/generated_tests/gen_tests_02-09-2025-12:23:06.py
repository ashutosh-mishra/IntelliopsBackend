import unittest
import requests

class TestUserAPI(unittest.TestCase):

    BASE_URL = 'http://localhost:5000'
    HEADERS = {'Content-Type': 'application/json'}

    def test_create_user(self):
        payload = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        response = requests.post(f'{self.BASE_URL}/users', headers=self.HEADERS, json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'John Doe')
        self.assertEqual(response.json()['email'], 'john.doe@example.com')

    def test_get_user(self):
        user_id = '123e4567-e89b-12d3-a456-426614174000'
        response = requests.get(f'{self.BASE_URL}/users/{user_id}', headers=self.HEADERS)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], user_id)
        self.assertEqual(response.json()['name'], 'John Doe')
        self.assertEqual(response.json()['email'], 'john.doe@example.com')


class TestCompanyAPI(unittest.TestCase):

    BASE_URL = 'http://localhost:5000'
    HEADERS = {'Content-Type': 'application/json'}

    def test_create_company(self):
        payload = {'name': 'Acme Corp', 'userId': '123e4567-e89b-12d3-a456-426614174000'}
        response = requests.post(f'{self.BASE_URL}/companies', headers=self.HEADERS, json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Acme Corp')
        self.assertEqual(response.json()['userId'], '123e4567-e89b-12d3-a456-426614174000')

    def test_get_company(self):
        company_id = '987e6543-b21c-45d3-a456-426614174111'
        response = requests.get(f'{self.BASE_URL}/companies/{company_id}', headers=self.HEADERS)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], company_id)
        self.assertEqual(response.json()['name'], 'Acme Corp')
        self.assertEqual(response.json()['userId'], '123e4567-e89b-12d3-a456-426614174000')


class TestWorkflowAPI(unittest.TestCase):

    BASE_URL = 'http://localhost:5000'
    HEADERS = {'Content-Type': 'application/json'}

    def test_user_company_workflow(self):
        # Create a user
        user_payload = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        user_response = requests.post(f'{self.BASE_URL}/users', headers=self.HEADERS, json=user_payload)

        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json()['id']

        # Create a company with the created user
        company_payload = {'name': 'Acme Corp', 'userId': user_id}
        company_response = requests.post(f'{self.BASE_URL}/companies', headers=self.HEADERS, json=company_payload)

        self.assertEqual(company_response.status_code, 201)
        self.assertEqual(company_response.json()['userId'], user_id)

        # Get the user and validate
        get_user_response = requests.get(f'{self.BASE_URL}/users/{user_id}', headers=self.HEADERS)

        self.assertEqual(get_user_response.status_code, 200)
        self.assertEqual(get_user_response.json()['id'], user_id)

        # Get the company and validate
        company_id = company_response.json()['id']
        get_company_response = requests.get(f'{self.BASE_URL}/companies/{company_id}', headers=self.HEADERS)

        self.assertEqual(get_company_response.status_code, 200)
        self.assertEqual(get_company_response.json()['id'], company_id)
        self.assertEqual(get_company_response.json()['userId'], user_id)

if __name__ == '__main__':
    unittest.main()