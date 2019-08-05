FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /interview_calendar
WORKDIR /interview_calendar
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
