# Use NVIDIA's CUDA enabled Ubuntu base image
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# Set the working directory in the container
WORKDIR /app

# Install required packages and Python 3.10
RUN apt-get update && \
    apt-get install -y software-properties-common wget && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-distutils libcudnn8 libcudnn8-dev && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    apt-get update && \
    apt-get install -y ffmpeg && \
    python3.10 get-pip.py && \
    rm get-pip.py && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Copy the requirements.txt file into the working directory
COPY requirements.txt .

# Install Python requirements
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

# Copy the entire backend application to the container
COPY . .

# Make the custom entrypoint script executable
RUN chmod +x /app/scripts/start-backend.local.sh

# Expose the port your application runs on
EXPOSE 8000

# Specify the custom entrypoint script
ENTRYPOINT ["/app/scripts/start-backend.local.sh"]

# CMD can be used to provide default arguments to the ENTRYPOINT if needed
# CMD ["arg1", "arg2"]  # Uncomment and modify this line if arguments are required
