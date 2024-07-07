FROM --platform=amd64 python:3.12.4


RUN apt-get update -y && apt-get upgrade -y 





COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "." ]

