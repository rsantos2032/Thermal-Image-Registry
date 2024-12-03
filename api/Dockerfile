FROM python:3.12.2
WORKDIR /app
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
