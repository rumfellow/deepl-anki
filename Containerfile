FROM python:3.11-slim

# Create non-privileged user
RUN useradd -m -u 1000 -s /bin/bash appuser

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

# Change ownership to non-privileged user
RUN chown -R appuser:appuser /app

# Switch to non-privileged user
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
