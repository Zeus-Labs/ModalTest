from loguru import logger
import sys
logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

logger.debug("logger set up")
import torch
logger.debug("import torch")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
logger.debug("setup torch device")
loaded_tensor = torch.load('./torch_tensor.pt', map_location=device)
logger.debug("loaded tensor")

import os
logger.debug(f"Size of torch_tensor.pt {os.path.getsize('torch_tensor.pt')}")

