#!/bin/bash

# AusflugAgypten Deployment Script
# Run this script to deploy updates to the production server

set -e  # Exit on error

echo "🚀 Starting AusflugAgypten deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/var/www/ausflugagypten"
BACKEND_DIR="$PROJECT_DIR/backend"
VENV_DIR="$BACKEND_DIR/venv"

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as correct user
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run this script as root"
    exit 1
fi

# Navigate to project directory
cd $PROJECT_DIR || exit 1

# 1. Pull latest code
print_message "Pulling latest code from repository..."
git pull origin main

# 2. Build frontend
print_message "Building frontend assets..."
npm install
npm run build

# 3. Activate virtual environment
print_message "Activating Python virtual environment..."
source $VENV_DIR/bin/activate

# 4. Install/Update Python dependencies
print_message "Installing Python dependencies..."
cd $BACKEND_DIR
pip install -r requirements.txt --quiet

# 5. Run migrations
print_message "Running database migrations..."
python manage.py migrate --noinput

# 6. Collect static files
print_message "Collecting static files..."
python manage.py collectstatic --noinput --clear

# 7. Check for issues
print_message "Running Django checks..."
python manage.py check --deploy

# 8. Restart Gunicorn
print_message "Restarting Gunicorn service..."
sudo systemctl restart gunicorn-ausflug

# 9. Reload Nginx
print_message "Reloading Nginx..."
sudo systemctl reload nginx

# 10. Check service status
print_message "Checking service status..."
if systemctl is-active --quiet gunicorn-ausflug; then
    print_message "✅ Gunicorn is running"
else
    print_error "❌ Gunicorn is not running"
    sudo systemctl status gunicorn-ausflug
    exit 1
fi

if systemctl is-active --quiet nginx; then
    print_message "✅ Nginx is running"
else
    print_error "❌ Nginx is not running"
    sudo systemctl status nginx
    exit 1
fi

print_message "🎉 Deployment completed successfully!"
print_message "Website: https://ausflugagypten.com"
print_message "Admin: https://ausflugagypten.com/admin/"

# Optional: Show recent logs
print_message "Recent Gunicorn logs:"
sudo journalctl -u gunicorn-ausflug -n 10 --no-pager


