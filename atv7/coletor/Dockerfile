FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Cria o ambiente virtual e instala dependências nele
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# Define o Python e Pip do ambiente virtual explicitamente
ENV PATH="/app/venv/bin:$PATH"

CMD ["python", "coletor.py"]
