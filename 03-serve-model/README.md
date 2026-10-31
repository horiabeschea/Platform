# Lesson 3: TensorFlow Serving

Read [the article on Medium](https://medium.com/@horiabe/serving-a-model-is-a-contract-not-just-a-container-19673992d66d?sharedUserId=horiabe). Train the model in lesson one first and install its TensorFlow dependency in your environment. From this folder:

```bash
python export.py
```

The export is written to `models/classifier/1`; choose another `--output` if the directory exists. To verify it locally without Docker:

```bash
python -c "import numpy as np,tensorflow as tf; x=tf.zeros((1,96,96,3)); m=tf.keras.models.load_model('../01-train-classifier/output/classifier.keras',compile=False); s=tf.saved_model.load('models/classifier/1'); np.testing.assert_allclose(m(x).numpy(),s.signatures['serving_default'](image=x)['scores'].numpy(),rtol=1e-5,atol=1e-5); print('SavedModel parity passed')"
```

With Docker running, mount the absolute path to `models/classifier` as `/models/classifier` and run `tensorflow/serving` with `MODEL_NAME=classifier` and host port `8501` mapped to container port `8501`. On a Unix shell:

```bash
docker run --rm -p 8501:8501 --mount "type=bind,source=$(pwd)/models/classifier,target=/models/classifier,readonly" -e MODEL_NAME=classifier tensorflow/serving
```

In a second terminal run `python check_serving.py`. On Windows use the absolute source path and your shell's syntax. The model server container is an external dependency; a running daemon and access to the image are required. This example uses an unpinned teaching image; pin and verify the image for a real deployment.
