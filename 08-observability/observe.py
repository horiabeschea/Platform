"""Simulate queue and service duration without external services."""
import argparse
import json
import time
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('--queue-delay', type=float, default=0.2)
parser.add_argument('--model-delay', type=float, default=0.1)
args = parser.parse_args()
if args.queue_delay < 0 or args.model_delay < 0:
    parser.error('delays must be non-negative')
job_id = str(uuid.uuid4())
queued = time.monotonic()
time.sleep(args.queue_delay)
started = time.monotonic()
time.sleep(args.model_delay)
finished = time.monotonic()
print(json.dumps({'job_id': job_id, 'queue_wait_seconds': round(started - queued, 3),
                  'model_seconds': round(finished - started, 3),
                  'total_seconds': round(finished - queued, 3)}))
