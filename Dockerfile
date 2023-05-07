FROM ubuntu:20.04

RUN apt-get update -y 

RUN apt-get upgrade -y

RUN apt-get install python3.7.2 -y

RUN apt-get install python3-pip -y

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 1001

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=1001", "--reload"]