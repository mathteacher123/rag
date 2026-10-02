# Use an official Python 3.12 slim image to match your Codespace environment
FROM python:3.12-slim

# Set a distinct working directory inside the container to avoid name clashes
WORKDIR /workspace

# Copy dependency definition first to optimize Docker layer caching
COPY requirements.txt .

# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from 'rag/' (including your 'app/' directory) into '/workspace'
COPY . .

# Inform Docker that the container will listen on a port at runtime
EXPOSE 8080

# Run Chainlit, binding to all interfaces and injecting Render's dynamic $PORT env variable
CMD ["sh", "-c", "chainlit run app/chat.py --host 0.0.0.0 --port ${PORT:-8080}"]
