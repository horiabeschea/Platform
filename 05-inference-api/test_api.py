import io
import json
import unittest
from unittest.mock import patch
from app import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.image = [[[0, 0, 0] for _ in range(96)] for _ in range(96)]

    def test_rejects_invalid_and_oversized(self):
        self.assertEqual(self.client.post('/v1/predict', json={'image': []}).status_code, 400)
        self.assertEqual(self.client.post('/v1/predict', data='x' * 500001,
                                         content_type='application/json').status_code, 413)

    def test_backend_failure_is_reported(self):
        with patch('app.urllib.request.urlopen', side_effect=OSError('down')):
            response = self.client.post('/v1/predict', json={'image': self.image})
        self.assertEqual(response.status_code, 502)

    def test_invalid_backend_scores_fail_closed(self):
        for scores in ([None, 'bad'], [float('nan'), 0.5], [1.1, 0.5], [True, 0.5]):
            with self.subTest(scores=scores):
                body = io.BytesIO(json.dumps({'predictions': [scores]}).encode())
                with patch('app.urllib.request.urlopen', return_value=body):
                    response = self.client.post('/v1/predict', json={'image': self.image})
                self.assertEqual(response.status_code, 502)

    def test_success_maps_label_order(self):
        body = io.BytesIO(json.dumps({'predictions': [[0.2, 0.8]]}).encode())
        with patch('app.urllib.request.urlopen', return_value=body):
            response = self.client.post('/v1/predict', json={'image': self.image})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['labels'], {'odd': 0.2, 'at_least_five': 0.8})


if __name__ == '__main__':
    unittest.main()
