"""Local demonstration: enqueue a pure, repeatable inference stand-in."""
import os
import time
from celery import Celery
from flask import Flask, jsonify, request

redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
celery = Celery('lesson', broker=redis_url, backend=redis_url)
app = Flask(__name__)

@celery.task
def predict(value):
    time.sleep(2)  # Represents a slow model call; this is not ML inference.
    return {'label': 'high' if value >= 0.5 else 'low'}

@app.post('/jobs')
def submit():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get('value'), (int, float)) or isinstance(data['value'], bool) or not 0 <= data['value'] <= 1:
        return jsonify(error='value must be a number in [0, 1]'), 400
    task = predict.delay(data['value'])
    return jsonify(job_id=task.id), 202

@app.get('/jobs/<job_id>')
def status(job_id):
    result = celery.AsyncResult(job_id)
    body = {'job_id': job_id, 'state': result.state}
    if result.successful():
        body['result'] = result.result
    elif result.failed():
        body['error'] = 'job failed'
    return jsonify(body)
