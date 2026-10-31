# Deploy an API and Model Server to Kubernetes

**Audience:** Developers with basic container knowledge.

## Article idea

Package and deploy the API and model server using Deployments and Services. Explain configuration, model storage, GPU scheduling where needed, resource requests, readiness checks, and a local smoke test.


## Agent-assisted exercise

**Task:** Ask an agent to deploy the API and model server to Kubernetes.

**Verify and decide:** Inspect generated resources, then test whether readiness reflects a usable model, verify service wiring, and exercise a failed rollout or unavailable model.

## Article and example

Read [the article on Medium](https://medium.com/@horiabe/your-kubernetes-pod-is-running-is-your-model-ready-22ff85531ab6?sharedUserId=horiabe). The sample uses mock HTTP services rather than a real model. Prerequisites: Docker, kubectl, and an existing local kind cluster named `kind`; adjust the cluster name if yours differs. Run from this folder in a shell:

```bash
docker build -t smallsteps-lesson:local .
kind load docker-image smallsteps-lesson:local --name kind
kubectl create namespace lesson-demo
kubectl apply -n lesson-demo -f deployment.yaml
kubectl rollout status -n lesson-demo deployment/lesson-model
kubectl rollout status -n lesson-demo deployment/lesson-api
kubectl port-forward -n lesson-demo deployment/lesson-api 18080:8080
```

In another terminal, run `curl -i http://127.0.0.1:18080/ready`. To simulate an unavailable model, run `kubectl set env -n lesson-demo deployment/lesson-model MODEL_READY=false` and observe `kubectl get pods -n lesson-demo -w`. Restore it with `kubectl set env -n lesson-demo deployment/lesson-model MODEL_READY=true`. A deployment port-forward targets the pod even if it becomes unready.

This example uses a mutable local image and has no inference, TLS, authentication, persistent model storage, or production hardening. A local process-level readiness check passed; image build and cluster deployment were not run because no Docker daemon was available.
