FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
# RUN python3 -m venv .
# RUN source bin/activate
RUN pip3 install -r requirements.txt

COPY assinante.py .

CMD ["python3", "assinante.py"]