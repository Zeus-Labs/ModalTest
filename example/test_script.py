print("Inside test_script.py")
from loguru import logger
import sys
logger.remove(0)
logger.add(sys.stderr, level="DEBUG")
logger.debug("logger set up")


# Simulating imports before torch import
# Imports in main_asr_stream.py before torch
import argparse
import asyncio

# Imports in provider stream before torch
import os
logger.debug("starting import cv2")
import cv2
logger.debug("finished import cv2")
import glob
import json
import tqdm
import numpy as np

# Imports in audio stream before torch
import asyncio
from pydub import AudioSegment
logger.debug("starting import torch")
import torch
logger.debug("finished import torch")

logger.debug("starting from scipy")
from scipy import signal
logger.debug("finished from scipy")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
logger.debug("setup torch device")
loaded_tensor = torch.load('./torso_imgs_tensor.pt', map_location=device)
logger.debug("loaded tensor")

logger.debug(f"Size of torch_tensor.pt {os.path.getsize('torso_imgs_tensor.pt')}")
