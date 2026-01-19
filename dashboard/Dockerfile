FROM python:3.14-alpine3.23

WORKDIR /usr/src/app

RUN apk add --no-cache iproute2 traceroute curl

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
