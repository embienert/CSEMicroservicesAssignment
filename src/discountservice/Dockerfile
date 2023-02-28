FROM python:3.8

WORKDIR /app

COPY dependencies.txt dependencies.txt

RUN python -m pip install --upgrade pip

RUN pip install -r dependencies.txt

COPY . .

CMD ["python3", "server.py"]