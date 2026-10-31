import argparse
from pathlib import Path
import tensorflow as tf


def export(model_path, export_path):
    model = tf.keras.models.load_model(model_path, compile=False)
    class ServingModel(tf.Module):
        def __init__(self, classifier):
            super().__init__()
            self.classifier = classifier

        @tf.function(input_signature=[tf.TensorSpec([None, 96, 96, 3], tf.float32, name='image')])
        def serve(self, image):
            return {'scores': self.classifier(image, training=False)}

    module = ServingModel(model)
    tf.saved_model.save(module, str(export_path), signatures={'serving_default': module.serve})


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--model', default='../01-train-classifier/output/classifier.keras')
    p.add_argument('--output', type=Path, default=Path('models/classifier/1'))
    args = p.parse_args()
    if args.output.exists():
        p.error('Output already exists; use a new version directory')
    export(args.model, args.output)
