# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV type ""
ENV output_dir "./"

CMD ["sh", "-c", "python3 download_real_time.py -t=${type} -o=${output_dir}"]
