# pull official base image
FROM python:3.13

# set work directory
WORKDIR /app

# set environment variables: prevent python to write pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip && pip install uv
COPY . /app/
RUN uv venv && uv sync

# copy project

EXPOSE 8000

~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
"Dockerfile" 20L, 388B                                                                                                                                         14,21        Весь
