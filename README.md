# Smallsteps ML Platform Examples

Companion code for Horia Beschea's Smallsteps Medium series on building and evaluating an agent-assisted machine-learning platform. Article links are added as the posts become available.

| Lesson | Example | Medium post |
| --- | --- | --- |
| 1 | [Train a multi-label classifier](01-train-classifier/) | [Read on Medium](https://medium.com/@horiabe/train-a-multi-label-image-classifier-you-can-evaluate-1d857a56672e?sharedUserId=horiabe) |
| 2 | [Run repeatable inference](02-repeatable-inference/) | [Read on Medium](https://medium.com/@horiabe/your-model-loaded-successfully-are-the-predictions-still-meaningful-459e30f8037a?sharedUserId=horiabe) |
| 3 | [Serve a TensorFlow model](03-serve-model/) | [Read on Medium](https://medium.com/@horiabe/serving-a-model-is-a-contract-not-just-a-container-19673992d66d?sharedUserId=horiabe) |
| 4 | [Protect evaluation data in a feedback loop](04-feedback-and-retraining/) | [Read on Medium](https://medium.com/@horiabe/your-feedback-loop-can-make-your-test-score-lie-19cb9a4ac3e7) |
| 5 | [Build an inference API](05-inference-api/) | [Read on Medium](https://medium.com/@horiabe/give-your-model-api-a-contract-you-can-test-cbec701295a7?sharedUserId=horiabe) |
| 6 | [Deploy services to Kubernetes](06-kubernetes-deployment/) | [Read on Medium](https://medium.com/@horiabe/your-kubernetes-pod-is-running-is-your-model-ready-22ff85531ab6?sharedUserId=horiabe) |
| 7 | [Queue jobs with Celery](07-celery-workers/) | [Read on Medium](https://medium.com/@horiabe/a-celery-worker-does-not-automatically-make-an-api-asynchronous-5278ae28518b) |
| 8 | [Measure processing delays](08-observability/) | [Read on Medium](https://medium.com/@horiabe/a-slow-ml-job-has-more-than-one-clock-12148e3dc370) |
| 9 | [Check a model contract in CI](09-ci-and-delivery/) | Forthcoming |

## Getting started

Use Python 3.10–3.12 and an isolated virtual environment. Activate it using the command for your shell, then run the commands below from each lesson directory. Lesson 1 downloads MNIST and pretrained weights. Lessons 2 and 3 use the model created by lesson 1.

```bash
cd 01-train-classifier
python -m pip install -r requirements.txt
python train.py
```

To check inference, run `python check_parity.py` from `02-repeatable-inference/`. To export the model, run `python export.py` from `03-serve-model/`. The export creates a versioned SavedModel under `models/classifier/1`.

The other examples can be run independently:

- **Feedback:** `python feedback.py` in `04-feedback-and-retraining/` demonstrates protecting test IDs; it does not retrain a model.
- **API:** Install `05-inference-api/requirements.txt`, then run `python -m unittest test_api.py` or `python app.py` from that directory. A real inference call also needs the model server from lesson 3.
- **Kubernetes:** Build the `06-kubernetes-deployment/Dockerfile`, load the image into a local cluster, and apply `deployment.yaml` in a test namespace. The API and model are mock HTTP services.
- **Celery:** Install `07-celery-workers/requirements.txt` and start a local Redis server. Run `celery -A app.celery worker --loglevel=info --pool=solo` and `flask --app app run` in separate terminals from that directory.
- **Observability:** Run `python observe.py --queue-delay 0.2 --model-delay 0.1` from `08-observability/` to simulate processing times.
- **CI:** Run `python -m unittest -v test_contract` from `09-ci-and-delivery/`. Its Jenkinsfile contains a test gate and a promotion placeholder.

These examples are teaching material. They do not include the authentication, security controls, reliability, or production deployment configuration needed for a public service.
