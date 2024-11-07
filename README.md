## Overview

A toy example to test out performance on Modal.

These are the key steps that happen:
- In `modal_deployment.py` file a CUDA container image is created with some system dependencies
- Inside `example_function`, CPU and GPU memory usage is monitored for every 5 seconds.

## Setup and Run
In your python environment, do the following:
```
pip install modal
modal setup
modal run modal_deployment.py
```
