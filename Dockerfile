FROM python:3.9-slim-buster

# Atualiza o sistema e instala dependências
RUN apt update && apt upgrade -y

# Cria um usuário não-root
RUN useradd -m appuser

# Cria o diretório da aplicação e muda a propriedade para o novo usuário
RUN mkdir /app/ && chown appuser:appuser /app/

# Define o diretório de trabalho
WORKDIR /app/

# Copia os arquivos da aplicação para o diretório de trabalho
COPY --chown=appuser:appuser . /app/

# Cria um ambiente virtual
RUN python -m venv venv

# Ativa o ambiente virtual e instala as dependências
USER appuser
RUN . venv/bin/activate && pip install --upgrade pip && pip install -U -r requirements.txt

# Define o comando para executar a aplicação
CMD ["venv/bin/python", "suapbot/__main__.py"]
