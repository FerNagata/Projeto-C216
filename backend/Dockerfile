FROM python:3.10-slim

WORKDIR /app

COPY ./src .
COPY requirements.txt .

RUN pip install -r "requirements.txt"

CMD ["python", "main.py"]