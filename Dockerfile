FROM python:3.8-slim

COPY my_bot.py /app/my_bot.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "main.py"]
