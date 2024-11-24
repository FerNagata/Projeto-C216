FROM python:3.10-slim

RUN pip install flask requests

WORKDIR /app
COPY . /app

EXPOSE 3000

CMD ["python", "app.py"]