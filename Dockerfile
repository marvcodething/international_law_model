# Use Python 3.11 slim image for smaller size and security
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first for better Docker layer caching
# This allows Docker to cache the pip install step if requirements haven't changed
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir prevents pip from keeping cache, reducing image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Set environment variables for Streamlit configuration
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Command to run when container starts
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]