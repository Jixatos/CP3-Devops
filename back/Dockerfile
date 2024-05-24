FROM python:3.9-slim
RUN apt-get update -y
RUN apt-get install libpq-dev python-dev-is-python3 -y
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]