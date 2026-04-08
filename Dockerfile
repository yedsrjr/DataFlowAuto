FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*
ENV TZ=America/Sao_Paulo

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-root


RUN chmod +x executa_atualizacao.sh

CMD ["poetry", "run", "python", "dataflowpx/app.py"]