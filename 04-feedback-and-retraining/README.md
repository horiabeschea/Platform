# Lesson 4: Feedback and Test-Set Protection

Read [the article on Medium](https://medium.com/@horiabe/your-feedback-loop-can-make-your-test-score-lie-19cb9a4ac3e7). Run the synthetic example using Python 3.10 or newer:

```bash
python feedback.py
```

The script first prints an expected rejection for a protected test ID. It then creates `candidate.json` from baseline and reviewed, non-protected entries and asserts that no protected IDs are present. The example does not train, evaluate, or promote a model; it illustrates one data boundary. Exact IDs alone cannot identify duplicates or related images. Generated candidate data is ignored by Git.
