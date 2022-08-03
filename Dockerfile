FROM python:3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY ./data_engineer/setup/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /interview_code
WORKDIR /interview_code

ENV PYTHONPATH=/interview_code