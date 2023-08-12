FROM python:3.11 as base

WORKDIR /

# Install FFmpeg for convert codecs
RUN apt-get update && apt-get install -y ffmpeg

# Download Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN mkdir /app/ /var/logs/ /var/static

COPY ./pyproject.toml poetry.lock /

# Include poetry into the path
ENV PATH="${PATH}:/root/.local/bin"

# Prevent poetry creating virtual environment before installing depedencies
RUN poetry config virtualenvs.create false

# Expose port for the application
EXPOSE 8000

### DEVELOPMENT ###
FROM base as development

# Install dependencies
# Use a Docker BuildKit cache mountto speed up the installation of Python dependencies
RUN --mount=type=cache,target=/root/.cache/poetry poetry install
COPY . .
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app", "--access-log"]


### PRODUCTION ###
FROM base as production

# Install dependencies
# Use a Docker BuildKit cache mountto speed up the installation of Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip poetry install --no-dev
COPY . .
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "app.api:app"]
