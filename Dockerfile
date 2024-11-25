FROM python:3.9-slim-buster

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN python -m venv venv
RUN . venv/bin/activate && pip install -U -r requirements.txt
CMD ["venv/bin/python", "suapbot/__main__.py"]
