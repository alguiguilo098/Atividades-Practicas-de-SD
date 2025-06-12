FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m venv ./ \
    source bin/activate \
    pip3 install -r requirements.txt

CMD ["python3", "coletor.py"]
