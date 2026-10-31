# Lesson 5: Inference API

The Medium article is forthcoming. Python 3.10+ is required. Install `python -m pip install -r requirements.txt`, then run `python app.py` from this folder. To call a real backend, first start the TensorFlow Serving example from lesson 3; set `MODEL_URL` if its address differs.

Run `python -m unittest test_api.py` to test invalid input, body size, backend failure, and a successful mocked response without a running model server. The example binds locally and has no authentication or production WSGI configuration. Do not expose it as a public service. A model promotion, artifact version, and label metadata contract are outside this example.
