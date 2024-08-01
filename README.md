## Overview

A toy example to test out performance on Modal.

These are the key steps that happen:
- The Dockerfile sets up an `example` conda environment, doing various pip installs.
- In `modal_deployment.py`, in the build step we additionally precompute a ~1GB tensor called `torso_imgs_tensor.pt` and store it on the image.
- When the modal function runs, it runs `example/test_script.py` in the `example` conda environment. The script does various imports -- notably importing torch. It sets up the cuda device, and it loads the `torso_imgs_tensor.pt`. It also logs the size of this tensor file.

## Setup and Run
In your python environment, do the following:
```
pip install modal
modal setup
modal run modal_deployment.py
```