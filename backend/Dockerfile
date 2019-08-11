FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /calendar
WORKDIR /calendar
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
