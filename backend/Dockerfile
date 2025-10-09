# Use the official Python image as a base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run Alembic migrations e iniciar FastAPI
CMD ["sh", "-c", "alembic -c alembic.ini upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
