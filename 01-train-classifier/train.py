"""Train a two-label image classifier using a frozen pretrained feature extractor."""
import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf

SIZE = 96
LABELS = ['odd', 'at_least_five']


def make_labels(digits):
    return np.column_stack((digits % 2 == 1, digits >= 5)).astype('float32')


def prepare_images(images):
    # Resize and replicate grayscale to RGB. The model rescales [0, 255] internally.
    images = tf.convert_to_tensor(images[..., None], dtype=tf.float32)
    return tf.image.grayscale_to_rgb(tf.image.resize(images, (SIZE, SIZE)))


def build_model(weights='imagenet'):
    backbone = tf.keras.applications.MobileNetV2(
        input_shape=(SIZE, SIZE, 3), include_top=False, weights=weights)
    backbone.trainable = False
    image = tf.keras.Input(shape=(SIZE, SIZE, 3), name='image')
    x = tf.keras.layers.Rescaling(1 / 127.5, offset=-1)(image)
    x = backbone(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(len(LABELS), activation='sigmoid', name='labels')(x)
    model = tf.keras.Model(image, outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy')
    return model


def report(labels, probabilities, threshold=0.5):
    predictions = probabilities >= threshold
    for index, name in enumerate(LABELS):
        actual = labels[:, index].astype(bool)
        predicted = predictions[:, index]
        tp = int(np.sum(actual & predicted))
        fp = int(np.sum(~actual & predicted))
        fn = int(np.sum(actual & ~predicted))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        print(f'{name}: precision={precision:.3f} recall={recall:.3f} support={int(actual.sum())}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--train-size', type=int, default=1024)
    parser.add_argument('--validation-size', type=int, default=256)
    parser.add_argument('--test-size', type=int, default=256)
    parser.add_argument('--epochs', type=int, default=2)
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--output', type=Path, default=Path('output'))
    args = parser.parse_args()
    if not (1 <= args.train_size <= 50000 and 1 <= args.validation_size <= 10000 and
            1 <= args.test_size <= 10000 and args.epochs > 0 and args.batch_size > 0):
        parser.error('sizes or training arguments are outside the supported range')

    tf.keras.utils.set_random_seed(42)
    (train_images, train_digits), (test_images, test_digits) = tf.keras.datasets.mnist.load_data()
    # MNIST's test split remains untouched until final evaluation.
    rng = np.random.default_rng(42)
    order = rng.permutation(len(train_images))
    train_ids = order[:args.train_size]
    val_ids = order[50000:50000 + args.validation_size]
    test_ids = rng.permutation(len(test_images))[:args.test_size]
    model = build_model()
    best_loss = float('inf')
    best_weights = None
    for epoch in range(args.epochs):
        rng.shuffle(train_ids)
        for start in range(0, len(train_ids), args.batch_size):
            ids = train_ids[start:start + args.batch_size]
            model.train_on_batch(prepare_images(train_images[ids]), make_labels(train_digits[ids]))
        model.reset_metrics()
        for start in range(0, len(val_ids), args.batch_size):
            ids = val_ids[start:start + args.batch_size]
            model.test_on_batch(prepare_images(train_images[ids]), make_labels(train_digits[ids]))
        loss = float(model.metrics[0].result())
        print(f'epoch {epoch + 1}: validation loss={loss:.4f}')
        if loss < best_loss:
            best_loss, best_weights = loss, model.get_weights()
    model.set_weights(best_weights)
    predictions = []
    for start in range(0, len(test_ids), args.batch_size):
        ids = test_ids[start:start + args.batch_size]
        predictions.append(model(prepare_images(test_images[ids]), training=False).numpy())
    report(make_labels(test_digits[test_ids]), np.concatenate(predictions))
    args.output.mkdir(parents=True, exist_ok=True)
    model.save(args.output / 'classifier.keras')
    (args.output / 'labels.json').write_text(json.dumps(LABELS, indent=2), encoding='utf-8')
    print(f'Saved model and label order in {args.output}')


if __name__ == '__main__':
    main()
