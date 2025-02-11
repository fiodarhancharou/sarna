# Use the arm64v8/python base image
# arm64v8/python:3.12.9-slim
FROM python:3.12.8-slim

# Set the working directory
WORKDIR /app

# Install Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get remove -y curl && \
    rm -rf /var/lib/apt/lists/*

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install the dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .


# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "sarna.main:app", "--host", "0.0.0.0", "--port", "8000"]
