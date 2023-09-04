import unittest
from app import app

class TestAPIService(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_categories(self):
        response = self.app.get('/categories')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_get_data_by_category(self):
        response = self.app.get('/data/SomeCategory')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_data_by_category_with_search(self):
        response = self.app.get('/data/SomeCategory?search_query=music')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
