FROM python:3.11-slim

# set environment variables
# Prevents Python from writing pyc files to disc 
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr 
ENV PYTHONUNBUFFERED 1

WORKDIR /

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.options.system-site-packages true
RUN echo poetry --version

# add all files
ADD . /app
WORKDIR /app

# # install dependencies
# RUN poetry install --all-extras

CMD ["bash"]
