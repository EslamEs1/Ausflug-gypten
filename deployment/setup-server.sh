#!/bin/bash

# AusflugAgypten Server Setup Script
# Run this script on a fresh Ubuntu server to set up the complete environment

set -e  # Exit on error

echo "🚀 Setting up AusflugAgypten server..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_message() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Update system
print_message "Updating system packages..."
apt update && apt upgrade -y

# Install required packages
print_message "Installing required packages..."
apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    curl \
    ufw \
    certbot \
    python3-certbot-nginx

# Install Node.js
print_message "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Configure PostgreSQL
print_message "Configuring PostgreSQL..."
sudo -u postgres psql <<EOF
CREATE DATABASE ausflug_egypt_prod;
CREATE USER ausflug_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
ALTER ROLE ausflug_user SET client_encoding TO 'utf8';
ALTER ROLE ausflug_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ausflug_user SET timezone TO 'Africa/Cairo';
GRANT ALL PRIVILEGES ON DATABASE ausflug_egypt_prod TO ausflug_user;
\q
EOF

# Create application directory
print_message "Creating application directory..."
mkdir -p /var/www/ausflugagypten
chown $SUDO_USER:$SUDO_USER /var/www/ausflugagypten

# Create log directory
print_message "Creating log directory..."
mkdir -p /var/log/ausflugagypten
chown www-data:www-data /var/log/ausflugagypten

# Configure firewall
print_message "Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Copy systemd service files
print_message "Installing systemd service files..."
cp /var/www/ausflugagypten/deployment/gunicorn.socket /etc/systemd/system/gunicorn-ausflug.socket
cp /var/www/ausflugagypten/deployment/gunicorn.service /etc/systemd/system/gunicorn-ausflug.service

# Copy Nginx configuration
print_message "Installing Nginx configuration..."
cp /var/www/ausflugagypten/deployment/nginx-ausflugagypten.conf /etc/nginx/sites-available/ausflugagypten
ln -sf /etc/nginx/sites-available/ausflugagypten /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
print_message "Testing Nginx configuration..."
nginx -t

# Reload systemd
print_message "Reloading systemd..."
systemctl daemon-reload

# Enable and start services
print_message "Enabling and starting services..."
systemctl enable gunicorn-ausflug.socket
systemctl start gunicorn-ausflug.socket
systemctl enable nginx
systemctl restart nginx

print_message "✅ Server setup completed!"
print_message ""
print_message "Next steps:"
print_message "1. Clone your repository to /var/www/ausflugagypten"
print_message "2. Create .env file in /var/www/ausflugagypten/backend/"
print_message "3. Run: cd /var/www/ausflugagypten/backend && python3.11 -m venv venv"
print_message "4. Run: source venv/bin/activate && pip install -r requirements.txt"
print_message "5. Run: python manage.py migrate"
print_message "6. Run: python manage.py collectstatic"
print_message "7. Run: python manage.py createsuperuser"
print_message "8. Run: sudo systemctl restart gunicorn-ausflug"
print_message "9. Get SSL certificate: sudo certbot --nginx -d ausflugagypten.com -d www.ausflugagypten.com"
print_message ""
print_message "⚠️  Don't forget to:"
print_message "- Update PostgreSQL password in .env"
print_message "- Set DEBUG=False in .env"
print_message "- Set SECRET_KEY in .env"
print_message "- Configure ALLOWED_HOSTS in .env"

