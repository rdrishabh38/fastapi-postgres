FROM python:3.11-slim

# Install git to clone the repository
RUN apt-get update && apt-get install -y git netcat-openbsd

# Clone the latest FastAPI project from GitHub
RUN git clone https://github.com/rdrishabh38/fastapi-postgres.git /fastapi-postgres

# Set the working directory to the project root
WORKDIR /fastapi-postgres

# Create a virtual environment inside the project
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip

# Install dependencies inside the virtual environment
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# "Activate" the virtual environment by adding its bin directory to PATH
ENV PATH="/fastapi-postgres/venv/bin:$PATH"

# Expose FastAPI's default port
EXPOSE 8000

RUN chmod +x /fastapi-postgres/entrypoint.sh

# Use the entrypoint script as the container's entrypoint
ENTRYPOINT ["/fastapi-postgres/entrypoint.sh"]

# Run FastAPI using uvicorn (which will now be found via the updated PATH)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
