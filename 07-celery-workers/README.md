# Use Celery for Long-Running Inference Jobs

**Audience:** API developers handling work that outlasts an HTTP request.

## Article idea

Move slow work behind a broker and worker, return a job ID, and expose job status. Explain queue isolation, retry behavior, timeouts, idempotency, and how waiting immediately for a Celery result changes the client experience.


## Agent-assisted exercise

**Task:** Ask an agent to move long-running inference into a Celery worker.

**Verify and decide:** Check whether the request actually returns a job ID promptly, then exercise worker failure, repeated delivery, and status reporting. Explain when idempotency is needed.

## Article and local example

The Medium article is forthcoming. Use Python 3.10+ and a local Redis server. In a new environment, install `python -m pip install -r requirements.txt`. Start Redis, then in separate terminals from this folder run:

```bash
celery -A app.celery worker --loglevel=info --pool=solo
flask --app app run --port 5000
curl -X POST http://127.0.0.1:5000/jobs -H "Content-Type: application/json" -d '{"value":0.8}'
curl http://127.0.0.1:5000/jobs/REPLACE_WITH_JOB_ID
```

The commands use POSIX quoting. `--pool=solo` is convenient for a local demo and does not represent production concurrency. Redis defaults to localhost; set `REDIS_URL` for a different local instance. The endpoint uses a dummy threshold, not a model. The example has no authentication or durable business job registry; use only in a trusted local environment. Input validation, mocked submission, and task logic were checked locally. Redis-backed integration was not run.
