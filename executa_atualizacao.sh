#!/bin/bash

# Arquivo de log
LOG_FILE="/home/administrador/Documentos/DataFlowPx/log_cron.txt"

# Adiciona data e hora de início
echo "--------------------------------------------------" >> "$LOG_FILE"
start_time=$(date +%s)
echo "Execução iniciada em: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# Carrega ambiente
source ~/.bashrc

echo "Fuso horário atual: $(cat /etc/timezone)" >> "$LOG_FILE"
echo "Data/hora atual: $(date)" >> "$LOG_FILE"

# Acessa pasta do projeto
cd /home/administrador/Documentos/DataFlowPx || {
  echo "Erro: pasta do projeto não encontrada" >> "$LOG_FILE"
  exit 1
}

# Executa o script via poetry
/home/administrador/.local/bin/poetry run python3 dataflowpx/app.py >> "$LOG_FILE" 2>&1
exit_code=$?

# Tempo de término
end_time=$(date +%s)
duration=$((end_time - start_time))
minutes=$((duration / 60))
seconds=$((duration % 60))

# Log final com sucesso ou erro + tempo de execução
if [ $exit_code -eq 0 ]; then
  echo "✅ Execução finalizada com sucesso: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
else
  echo "❌ Erro durante a execução: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
fi

echo "⏱️ Tempo de execução: ${minutes} min ${seconds} seg" >> "$LOG_FILE"
echo "--------------------------------------------------" >> "$LOG_FILE"

