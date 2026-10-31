# Add CI and Safe Delivery to an ML Service

**Audience:** Teams preparing an ML service for repeatable deployments.

## Article idea

Build a pipeline that runs focused tests, builds images, and validates the model contract. Describe versioned artifacts, controlled promotion, deployment checks, and rollback; distinguish application CI from retraining and model approval.


## Agent-assisted exercise

**Task:** Ask an agent to create CI and deployment checks for the ML service.

**Verify and decide:** Introduce a contract mismatch or failing test and verify that promotion stops. Inspect artifact versions and demonstrate a rollback or explain its prerequisites.

## Article and example

Read [the article on Medium](https://medium.com/@horiabe/a-passing-build-is-not-evidence-that-your-ml-contract-still-works-4a7f81dcb24c). Run `python -m unittest -v test_contract` from this directory with Python 3.10+. The accompanying Jenkinsfile is an illustrative pipeline with a test stage and a promotion placeholder. It requires a Unix-like Jenkins agent with Python 3 and the repository checked out. It does not build or deploy artifacts. Tests passed locally; Jenkins itself was not run.
