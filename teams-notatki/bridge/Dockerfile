FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

RUN useradd -r bridge && chown -R bridge:bridge /app
USER bridge

EXPOSE 8080
CMD ["python", "app.py"]
