import unittest
from app import app, get_secret, download_s3_file

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_boardgames(self):
        response = self.app.get('/boardgames')
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data

    def test_get_boardgame(self):
        response = self.app.get('/boardgames/123')
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data

    def test_search_boardgames(self):
        response = self.app.post('/search', json={"name": "Renature"})
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data

if __name__ == '__main__':
    unittest.main()