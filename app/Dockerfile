FROM python:3.9-slim

WORKDIR /app

# Instala as dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Cria e utiliza usuário não-root (requisito do CP)
RUN useradd -m gabiwu
USER gabiwu

EXPOSE 5000

CMD ["python", "app.py"]