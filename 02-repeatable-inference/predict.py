import argparse
import json
from pathlib import Path
import numpy as np
import tensorflow as tf

LABELS = ('odd', 'at_least_five')


def prepare_image(path):
    data = tf.io.read_file(str(path))
    image = tf.io.decode_image(data, channels=1, expand_animations=False)
    image = tf.image.resize(tf.cast(image, tf.float32), (96, 96))
    return tf.image.grayscale_to_rgb(image)


def predict(model, paths):
    if not paths:
        raise ValueError('Provide at least one image')
    probabilities = model(tf.stack([prepare_image(path) for path in paths]), training=False).numpy()
    if probabilities.shape != (len(paths), len(LABELS)):
        raise ValueError('Model output does not match the label contract')
    return [{label: float(value) for label, value in zip(LABELS, row)} for row in probabilities]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='../01-train-classifier/output/classifier.keras')
    parser.add_argument('images', nargs='+')
    args = parser.parse_args()
    model_path = Path(args.model)
    labels_path = model_path.with_name('labels.json')
    if json.loads(labels_path.read_text(encoding='utf-8')) != list(LABELS):
        raise ValueError('Label metadata does not match the expected contract')
    model = tf.keras.models.load_model(model_path, compile=False)
    print(json.dumps({'model': model_path.name, 'predictions': predict(model, args.images)}, indent=2))


if __name__ == '__main__':
    main()
