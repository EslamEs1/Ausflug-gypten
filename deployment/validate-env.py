#!/usr/bin/env python3
"""
Environment Validation Script for AusflugAgypten
Run this script to validate your environment configuration before deployment
"""

import os
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def print_error(message):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_success(f"{description} exists: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_env_variable(var_name, required=True, secret=False):
    """Check if environment variable is set"""
    value = os.environ.get(var_name)
    
    if value:
        if secret:
            print_success(f"{var_name} is set (hidden)")
        else:
            print_success(f"{var_name} = {value}")
        return True
    else:
        if required:
            print_error(f"{var_name} is not set (REQUIRED)")
        else:
            print_warning(f"{var_name} is not set (optional)")
        return required

def main():
    print("\n" + "="*60)
    print("AusflugAgypten Environment Validation")
    print("="*60 + "\n")
    
    errors = []
    warnings = []
    
    # Check Python version
    print_info("Checking Python version...")
    if sys.version_info >= (3, 11):
        print_success(f"Python version: {sys.version.split()[0]}")
    else:
        print_error(f"Python 3.11+ required, found: {sys.version.split()[0]}")
        errors.append("Python version")
    
    print()
    
    # Check required files
    print_info("Checking required files...")
    files_to_check = [
        ('backend/requirements.txt', 'Requirements file'),
        ('backend/manage.py', 'Django manage.py'),
        ('backend/config/settings.py', 'Django settings'),
        ('backend/config/wsgi.py', 'WSGI configuration'),
        ('package.json', 'Package.json'),
        ('tailwind.config.js', 'Tailwind config'),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            errors.append(f"Missing file: {filepath}")
    
    print()
    
    # Check .env file
    print_info("Checking .env file...")
    env_file = Path('backend/.env')
    if env_file.exists():
        print_success(".env file exists")
        
        # Load .env file
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    else:
        print_error(".env file not found!")
        errors.append("Missing .env file")
    
    print()
    
    # Check environment variables
    print_info("Checking environment variables...")
    
    # Required variables
    required_vars = [
        ('DEBUG', False),
        ('SECRET_KEY', True),
        ('ALLOWED_HOSTS', False),
        ('DB_NAME', False),
        ('DB_USER', False),
        ('DB_PASSWORD', True),
    ]
    
    for var_name, is_secret in required_vars:
        if not check_env_variable(var_name, required=True, secret=is_secret):
            errors.append(f"Missing required variable: {var_name}")
    
    # Optional variables
    optional_vars = [
        ('EMAIL_HOST', False),
        ('EMAIL_HOST_USER', False),
        ('EMAIL_HOST_PASSWORD', True),
        ('STRIPE_PUBLIC_KEY', False),
        ('STRIPE_SECRET_KEY', True),
        ('STRIPE_WEBHOOK_SECRET', True),
    ]
    
    for var_name, is_secret in optional_vars:
        if not check_env_variable(var_name, required=False, secret=is_secret):
            warnings.append(f"Optional variable not set: {var_name}")
    
    print()
    
    # Check DEBUG setting
    print_info("Checking production settings...")
    debug = os.environ.get('DEBUG', 'True').lower()
    if debug in ['false', '0', 'no']:
        print_success("DEBUG is False (production mode)")
    else:
        print_warning("DEBUG is True (development mode)")
        warnings.append("DEBUG should be False in production")
    
    # Check SECRET_KEY strength
    secret_key = os.environ.get('SECRET_KEY', '')
    if len(secret_key) >= 50:
        print_success(f"SECRET_KEY length: {len(secret_key)} characters")
    else:
        print_error(f"SECRET_KEY too short: {len(secret_key)} characters (should be 50+)")
        errors.append("Weak SECRET_KEY")
    
    # Check ALLOWED_HOSTS
    allowed_hosts = os.environ.get('ALLOWED_HOSTS', '')
    if 'localhost' in allowed_hosts or '127.0.0.1' in allowed_hosts:
        print_warning("ALLOWED_HOSTS contains localhost (should be removed in production)")
        warnings.append("ALLOWED_HOSTS contains localhost")
    
    print()
    
    # Check directory structure
    print_info("Checking directory structure...")
    dirs_to_check = [
        'backend/apps/core',
        'backend/apps/tours',
        'backend/apps/blog',
        'backend/apps/bookings',
        'backend/templates',
        'backend/static',
        'css',
        'js',
        'img',
        'fonts',
    ]
    
    for directory in dirs_to_check:
        if Path(directory).is_dir():
            print_success(f"Directory exists: {directory}")
        else:
            print_error(f"Directory not found: {directory}")
            errors.append(f"Missing directory: {directory}")
    
    print()
    
    # Summary
    print("="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    if errors:
        print(f"\n{Colors.RED}ERRORS ({len(errors)}):{Colors.END}")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print(f"\n{Colors.YELLOW}WARNINGS ({len(warnings)}):{Colors.END}")
        for warning in warnings:
            print(f"  • {warning}")
    
    if not errors and not warnings:
        print(f"\n{Colors.GREEN}✓ All checks passed! Environment is ready for deployment.{Colors.END}")
        return 0
    elif not errors:
        print(f"\n{Colors.YELLOW}⚠ Environment is ready but has warnings. Review them before deployment.{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}✗ Environment validation failed. Fix errors before deployment.{Colors.END}")
        return 1

if __name__ == '__main__':
    sys.exit(main())

