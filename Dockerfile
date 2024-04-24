FROM python:3.9

RUN pip install pika

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5672
EXPOSE 15672

EXPOSE 8000

CMD ["python", "/app/main.py"]
