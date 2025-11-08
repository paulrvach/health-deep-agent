# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project structure (needed for -e ../../ in requirements.txt)
# Copy root pyproject.toml and libs directory
COPY pyproject.toml /app/
COPY libs /app/libs

# Copy requirements and install dependencies
COPY examples/research/requirements.txt /app/examples/research/
WORKDIR /app/examples/research

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY examples/research/ /app/examples/research/

# Expose port 8000
EXPOSE 8000

# Run the server
WORKDIR /app/examples/research
CMD ["python", "server.py"]

