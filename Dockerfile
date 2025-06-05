# pull official base image
FROM python:3.13

# set work directory
WORKDIR /app

# set environment variables: prevent python to write pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip && pip install uv
COPY pyproject.toml uv.lock* /app/
RUN uv venv && uv sync

# copy project
COPY . /app/

EXPOSE 8000
