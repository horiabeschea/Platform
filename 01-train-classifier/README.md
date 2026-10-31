# Lesson 1: Train a Multi-Label Image Classifier

By Horia Beschea, Smallsteps. Read [the article on Medium](https://medium.com/@horiabe/train-a-multi-label-image-classifier-you-can-evaluate-1d857a56672e?sharedUserId=horiabe) for the lesson and design tradeoffs.

## Run

Use Python 3.10–3.12 and create an isolated environment. The first run downloads TensorFlow, MNIST, and ImageNet weights; training uses a CPU by default and can take several minutes.

```bash
python -m venv .venv
# Activate .venv for your shell, then:
python -m pip install -r requirements.txt
python train.py
```

For a quick pipeline check, use `python train.py --train-size 32 --validation-size 16 --test-size 16 --epochs 1 --batch-size 8`. This sample is too small for meaningful model evaluation.

The script writes `output/classifier.keras` and `output/labels.json`. It prints validation loss and per-label test precision, recall, and support at a threshold of 0.5. Inputs to the saved model are RGB tensors with shape `(batch, 96, 96, 3)` and pixel values in `[0, 255]`; `prepare_images` handles MNIST's grayscale conversion and resizing.

The example demonstrates transfer learning with a frozen pretrained feature extractor and independent labels. It uses public handwritten-digit data and does not reproduce a production model or its performance.

## Agent-assisted exercise

**Task:** Ask an agent to train and evaluate a multi-label classifier with a held-out test set.

**Verify and decide:** Inspect the split, label definitions, preprocessing, and per-label precision and recall. Demonstrate how a convincing aggregate score can hide a weak label; use a constructed case unless an actual agent run produces the issue.
