FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Cria venv e instala no ambiente virtual
RUN python3 -m venv venv && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt

COPY classificador.py .

# Adiciona o venv ao PATH
ENV PATH="/app/venv/bin:$PATH"

CMD ["python", "classificador.py"]
