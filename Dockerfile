FROM python:3.9-slim-buster
	
RUN apt update && apt upgrade -y && apt-get install postgresql -y && apt-get install clang -y
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN pip3 install -U -r requirements.txt
CMD python3 suapbot/__main__.py
