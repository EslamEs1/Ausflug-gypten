#!/bin/bash

# AusflugAgypten Backup Script
# Run this script daily via cron to backup database and media files

set -e

# Configuration
BACKUP_DIR="/var/backups/ausflugagypten"
DB_NAME="ausflug_egypt_prod"
DB_USER="ausflug_user"
MEDIA_DIR="/var/www/ausflugagypten/backend/media"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Starting backup at $(date)"

# Backup database
echo "Backing up database..."
PGPASSWORD=$DB_PASSWORD pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup media files
echo "Backing up media files..."
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $MEDIA_DIR .

# Delete old backups
echo "Cleaning up old backups..."
find $BACKUP_DIR -type f -name "db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -type f -name "media_*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Calculate backup sizes
DB_SIZE=$(du -h $BACKUP_DIR/db_$DATE.sql.gz | cut -f1)
MEDIA_SIZE=$(du -h $BACKUP_DIR/media_$DATE.tar.gz | cut -f1)

echo "Backup completed at $(date)"
echo "Database backup: $DB_SIZE"
echo "Media backup: $MEDIA_SIZE"
echo "Backups stored in: $BACKUP_DIR"

# Optional: Upload to remote storage (S3, etc.)
# aws s3 sync $BACKUP_DIR s3://your-bucket/ausflugagypten-backups/


