FROM ubuntu:22.04

# Set non-interactive frontend for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies including Node.js (v16+), Python3, FFmpeg
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    curl ffmpeg git python3 python3-pip python3-venv ca-certificates gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Default command to run the bot
CMD ["python3", "-m", "SHUKLA"]
