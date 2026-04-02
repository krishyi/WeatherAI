FROM python:3.11-slim

# Set working directory
WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Default command to run the AI helper script
CMD ["python", "ai_helper.py"]
