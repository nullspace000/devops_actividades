#!/bin/bash

# ID de la instancia que quieres gestionar
INSTANCIA_ID="i-0123456789abcdef0" # <--- REEMPLAZA CON TU ID REAL

# Obtener el día de la semana actual (1-7, donde 6 y 7 son fin de semana)
DIA_SEMANA=$(date +%u)

echo "=========================================="
echo "Iniciando mantenimiento de EC2: $(date)"
echo "=========================================="

# 1. Listar el estado actual de todas las instancias
echo "Estado actual de la región:"
python3 gestionar_ec2.py

# 2. Lógica de automatización por fin de semana
if [ "$DIA_SEMANA" -eq 6 ] || [ "$DIA_SEMANA" -eq 7 ]; then
    echo "Detección: Es fin de semana. Procediendo a detener la instancia por ahorro."
    python3 gestionar_ec2.py "$INSTANCIA_ID" detener
else
    echo "Detección: Es día laboral. No se realizarán paradas automáticas."
    # Opcional: Podrías poner aquí un comando para iniciarla si quieres que siempre esté prendida
    # python3 gestionar_ec2.py "$INSTANCIA_ID" iniciar
fi

echo "=========================================="
echo "Proceso finalizado con éxito."
