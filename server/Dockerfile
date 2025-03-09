FROM python:3.11-slim-bookworm AS builder

WORKDIR /app/server

# Install system dependencies for native modules (build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    clang \
    cmake \
    git \
    libopenblas-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python dependencies (including those requiring compilation)
RUN pip install --no-cache-dir --upgrade pip --force-reinstall && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir llama_cpp_python

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]