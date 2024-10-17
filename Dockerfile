FROM python:3.9-slim-buster
	
RUN apt update && apt upgrade -y
RUN apt install postgresql
RUN apt install clang
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN pip3 install -U -r requirements.txt
CMD python3 suapbot/__main__.py
