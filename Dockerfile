# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Ollama in background, pull the cloud bridge, then start Streamlit
CMD ["sh", "-c", "ollama serve & sleep 5 && ollama pull nemotron-3-nano:30b-cloud && streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
