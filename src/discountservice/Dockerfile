FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "server.py"]

EXPOSE 8080