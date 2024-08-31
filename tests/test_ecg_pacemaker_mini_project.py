import unittest
from app import app

class PacemakerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the ECG Pacemaker Classifier - Sagi Ezri', str(response.data))

    def test_predict_missing_metadata(self):
        response = self.app.post('/predict', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing fields in metadata', str(response.data))

    def test_predict_valid_request(self):
        test_metadata = {
            'age': 25,
            'recording_date': '31/08/2024 12:34:56',
            'height': 180,
            'weight': 75,
            'nurse': 1,
            'site': 2,
            'device': 'device1',
            'sex': 'M',
            'patient_id': '123456'
        }

        response = self.app.post('/predict', json=test_metadata, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pacemaker_result', str(response.data))

    def test_predict_age_under_18(self):
        test_metadata = {
            'age': 16,
            'recording_date': '31/08/2024 12:34:56'
        }

        response = self.app.post('/predict', json=test_metadata, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pacemaker_result', str(response.data))
        self.assertIn('None', str(response.data))

if __name__ == '__main__':
    unittest.main()
