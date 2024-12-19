# Use a imagem base com Python 3.11
FROM python:3.11-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do projeto para o diretório de trabalho
COPY . /app

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o aplicativo
CMD ["python", "main.py"]
