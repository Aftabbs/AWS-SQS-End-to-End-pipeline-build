FROM python:3.10-slim
WORKDIR /app
COPY api/api.py /app/
COPY shared /app/shared
COPY api/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
