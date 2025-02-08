import requests
import unittest
import uuid

class TestUserAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # assuming API is hosted locally

    def test_create_user(self):
        url = f"{self.BASE_URL}/users"
        data = {"name": "John Doe", "email": "john.doe@example.com"}
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 201)
        resp_data = response.json()
        self.assertIn('id', resp_data)
        self.assertIn('name', resp_data)
        self.assertEqual(resp_data['name'], data['name'])
        self.assertIn('email', resp_data)
        self.assertEqual(resp_data['email'], data['email'])
        return resp_data['id']

    def test_get_user(self):
        user_id = self.test_create_user()
        url = f"{self.BASE_URL}/users/{user_id}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertEqual(resp_data['id'], user_id)

class TestCompanyAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # assuming API is hosted locally

    def test_create_company(self):
        user_id = TestUserAPI().test_create_user()
        url = f"{self.BASE_URL}/companies"
        data = {"name": "Acme Corp", "userId": user_id}
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 201)
        resp_data = response.json()
        self.assertIn('id', resp_data)
        self.assertIn('name', resp_data)
        self.assertEqual(resp_data['name'], data['name'])
        self.assertIn('userId', resp_data)
        self.assertEqual(resp_data['userId'], data['userId'])
        return resp_data['id']

    def test_get_company(self):
        company_id = self.test_create_company()
        url = f"{self.BASE_URL}/companies/{company_id}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertEqual(resp_data['id'], company_id)

if __name__ == "__main__":
    unittest.main()