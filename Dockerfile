# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Streamlit and Ollama ports
EXPOSE 8501
EXPOSE 11434

# Set Environment Variables
ENV OLLAMA_BASE_URL=http://localhost:11434
ENV PYTHONUNBUFFERED=1

# Create a startup script
RUN echo '#!/bin/bash\n\
ollama serve & \n\
sleep 5\n\
echo "📥 Pulling model: nemotron-3-nano..." \n\
ollama pull nemotron-3-nano \n\
echo "🚀 Starting Streamlit..." \n\
streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0' > start.sh && chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]
