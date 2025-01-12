FROM python:3.10-slim
WORKDIR /app
COPY consumer/consumer.py /app/
COPY shared /app/shared
COPY consumer/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "consumer.py"]
