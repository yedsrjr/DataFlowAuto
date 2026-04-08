# DataFlowPx

Projeto de automação para consulta de dados em uma API SAP/Liberali e sincronização dessas informações com uma base PostgreSQL.

A ideia deste projeto é buscar os dados dos animais, tratar algumas informações e inserir ou atualizar os registros no banco de dados local.

## O que o projeto faz

- consulta dados em uma API externa
- formata campos como datas, sexo e status
- insere ou atualiza os animais na base de dados
- registra logs de sucesso e erro no banco

## Estrutura principal

- `dataflowpx/app.py`
  Responsável pelo fluxo principal da automação.

- `dataflowpx/auth.py`
  Faz a comunicação com a API externa.

- `dataflowpx/database.py`
  Cria a conexão e sessão com o banco usando SQLAlchemy.

- `dataflowpx/models.py`
  Define os modelos `Animal` e `LogInsercaoAnimais`.

- `dataflowpx/settings.py`
  Carrega as variáveis de ambiente com `pydantic-settings`.

- `Dockerfile`
  Arquivo para execução do projeto em container.

- `crontab.txt`
  Exemplo de agendamento da automação.

## Tecnologias utilizadas

- Python
- SQLAlchemy
- PostgreSQL
- Requests
- Pydantic Settings
- Poetry
- Docker

## Variáveis de ambiente

O projeto utiliza um arquivo `.env` com as seguintes variáveis:

```env
IP_API_LIBERALI=
AUTH_API_LIBERALI=
PATH_DATABASE=
```

## Como executar

### Ambiente local

```bash
poetry install
poetry run python dataflowpx/app.py
```

### Docker

```bash
docker build -t dataflowpx .
docker run --env-file .env dataflowpx
```

## Observação

Este projeto foi desenvolvido com foco em automação de integração de dados.

O repositório mantém os arquivos essenciais para execução da rotina, incluindo código-fonte, configuração do ambiente e arquivos de apoio para execução agendada.
