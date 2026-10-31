# Find Bottlenecks in an ML Processing Pipeline

**Audience:** Teams operating ML workloads.

## Article idea

Follow a job from API submission through queue, worker, and inference. Identify useful measurements such as queue wait, task duration, failures, model latency, and resource utilization. Explain how correlation IDs help diagnose a slow request.


## Agent-assisted exercise

**Task:** Ask an agent to instrument the request, queue, worker, and model server.

**Verify and decide:** Introduce a controlled delay or failure, follow a job ID through the pipeline, and check whether the metrics distinguish queue wait from inference time.

## Article and example

Read [the article on Medium](https://medium.com/@horiabe/a-slow-ml-job-has-more-than-one-clock-12148e3dc370). Run `python observe.py --queue-delay 0.2 --model-delay 0.1` and compare it with `python observe.py --queue-delay 1 --model-delay 0.1`. The JSON shows simulated durations and a job ID; it does not implement Prometheus or distributed tracing. A short run passed locally.
