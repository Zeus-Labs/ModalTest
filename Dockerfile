FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu20.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends wget \
    ffmpeg \
    portaudio19-dev \
    python3-pyaudio \
    gcc \
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

# Install torch and other deps for example environment
RUN pip install --no-cache-dir torch==2.1.0+cu121 torchvision==0.16.0+cu121 torchaudio==2.1.0 --extra-index-url https://download.pytorch.org/whl/cu121

# Install the requirements
COPY ./example/requirements.txt ./example
RUN pip install --no-cache-dir -r ./example/requirements.txt

# Install wheels
COPY ./example/wheels /wheels
RUN pip install /wheels/*.whl

# Deactivate the conda environment
SHELL ["/bin/bash", "-c"]

# Copy the application code
COPY . .

# Pre compile the script to byte code
RUN conda run -n example python -m compileall ./example
