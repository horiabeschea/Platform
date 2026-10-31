# Lesson 2: Repeatable Inference

Read [the article on Medium](https://medium.com/@horiabe/your-model-loaded-successfully-are-the-predictions-still-meaningful-459e30f8037a?sharedUserId=horiabe). Install lesson one's TensorFlow dependencies and create `../01-train-classifier/output/classifier.keras` and `labels.json` by running its training script. Use Python 3.10–3.12.

From this folder, create one MNIST sample and run the client:

```bash
python -c "import tensorflow as tf; (_, _), (x, _) = tf.keras.datasets.mnist.load_data(); tf.io.write_file('digit.png', tf.io.encode_png(x[0,:,:,None]))"
python predict.py digit.png
```

Verify preprocessing against the actual training function:

```bash
python check_parity.py
```

Delete `digit.png` when finished. Results are demonstration scores, not evidence of production performance. Image and label order must match the training contract; the filename in the output is not an immutable model version.
