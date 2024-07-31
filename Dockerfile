FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu20.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends wget \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh
ENV PATH="/opt/conda/bin:${PATH}"

# Set up example conda environment
RUN conda create -n example python==3.8.8 && \
    conda clean -afy

# Activate the example environment
SHELL ["conda", "run", "-n", "example", "/bin/bash", "-c"]

# Install PyTorch and CUDA dependencies for example environment
RUN pip install --no-cache-dir torch==2.1.0+cu121 torchvision==0.16.0+cu121 torchaudio==2.1.0 --extra-index-url https://download.pytorch.org/whl/cu121

# Deactivate the conda environment
SHELL ["/bin/bash", "-c"]

# Copy the application code
COPY ./test_script.py ./test_script.py

# Pre compile the script to byte code
RUN conda run -n example python -m compileall ./test_script.py

# Make test script executable
RUN chmod +x /app/test_script.py
