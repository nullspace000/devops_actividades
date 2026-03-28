#!/bin/bash

# --- Configuration ---
BUCKET_NAME="mi-bucket-ejemplo"
SOURCE_DIR="/home/ec2-user/data"  # Change this to the folder you want to back up
BACKUP_NAME="backup_$(date +%Y-%m-%d_%H%M%S).tar.gz"
LOG_FILE="backup.log"

# --- Execution ---
echo "--- Respaldo iniciado: $(date) ---" >> "$LOG_FILE"

# 1. Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: El directorio $SOURCE_DIR no existe." >> "$LOG_FILE"
    exit 1
fi

# 2. Create the compressed archive
# 'c' create, 'z' gzip, 'f' file
tar -czf "$BACKUP_NAME" "$SOURCE_DIR" >> "$LOG_FILE" 2>&1

# 3. Upload to S3 and check for success
if aws s3 cp "$BACKUP_NAME" "s3://$BUCKET_NAME/" >> "$LOG_FILE" 2>&1; then
    echo "SUCCESS: Respaldo $BACKUP_NAME subido correctamente." >> "$LOG_FILE"
    # Optional: Remove local backup file after successful upload to save space
    # rm "$BACKUP_NAME"
else
    echo "ERROR: Falló la subida a S3. Revisa los permisos o la conexión." >> "$LOG_FILE"
fi

echo "--- Fin del proceso: $(date) ---" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
