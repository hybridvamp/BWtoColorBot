FROM python:3.8-slim

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "main.py"]
