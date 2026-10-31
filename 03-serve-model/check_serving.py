import argparse
import json
import urllib.request
import numpy as np
import tensorflow as tf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='../01-train-classifier/output/classifier.keras')
    parser.add_argument('--url', default='http://localhost:8501/v1/models/classifier:predict')
    args = parser.parse_args()
    image = np.zeros((1, 96, 96, 3), dtype=np.float32)
    local = tf.keras.models.load_model(args.model, compile=False)(image, training=False).numpy()
    payload = json.dumps({'instances': image.tolist()}).encode('utf-8')
    request = urllib.request.Request(args.url, data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=10) as response:
        served = np.asarray(json.load(response)['predictions'])
    np.testing.assert_allclose(local, served, rtol=1e-5, atol=1e-5)
    print('Local and served predictions agree:', served.tolist())


if __name__ == '__main__':
    main()
