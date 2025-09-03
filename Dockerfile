# Base Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Atualiza pip e instala dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Porta que o Fly vai expor
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
