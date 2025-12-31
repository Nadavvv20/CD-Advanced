FROM python:3.10-slim

WORKDIR /app

RUN pip install flask

COPY app.py .

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

