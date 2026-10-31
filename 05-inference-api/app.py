import json
import math
import os
import urllib.error
import urllib.request
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500_000
URL = os.environ.get('MODEL_URL', 'http://localhost:8501/v1/models/classifier:predict')


def valid_image(image):
    return (isinstance(image, list) and len(image) == 96 and
            all(isinstance(row, list) and len(row) == 96 and
                all(isinstance(pixel, list) and len(pixel) == 3 and
                    all(isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 255
                        for v in pixel) for pixel in row) for row in image))


@app.post('/v1/predict')
def predict():
    body = request.get_json(silent=True)
    if not isinstance(body, dict) or not valid_image(body.get('image')):
        return jsonify(error='image must be a 96x96 RGB array with values in [0,255]'), 400
    payload = json.dumps({'instances': [body['image']]}).encode('utf-8')
    req = urllib.request.Request(URL, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.load(response)
        scores = result['predictions'][0]
        if (not isinstance(scores, list) or len(scores) != 2 or
                not all(isinstance(v, (int, float)) and not isinstance(v, bool) and
                        0 <= v <= 1 and math.isfinite(v) for v in scores)):
            raise ValueError('invalid model response')
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return jsonify(error='model service unavailable or returned invalid data'), 502
    return jsonify(model='classifier', labels={'odd': scores[0], 'at_least_five': scores[1]})


if __name__ == '__main__':
    app.run(port=8080)
