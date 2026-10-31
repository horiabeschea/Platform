import argparse
import sys
import numpy as np
import tensorflow as tf
from predict import prepare_image

sys.path.insert(0, '../01-train-classifier')
from train import prepare_images

p = argparse.ArgumentParser()
p.add_argument('--image', default='digit.png')
p.add_argument('--model', default='../01-train-classifier/output/classifier.keras')
args = p.parse_args()
(_, _), (images, _) = tf.keras.datasets.mnist.load_data()
training_input = prepare_images(images[:1])
inference_input = tf.expand_dims(prepare_image(args.image), 0)
np.testing.assert_allclose(training_input.numpy(), inference_input.numpy())
model = tf.keras.models.load_model(args.model, compile=False)
np.testing.assert_allclose(model(training_input, training=False).numpy(),
                           model(inference_input, training=False).numpy())
print('Preprocessing and model predictions match')
