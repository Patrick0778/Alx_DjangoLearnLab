#!/usr/bin/env python
"""
Security Testing Script for LibraryProject

This script performs basic security validation checks on the LibraryProject
to ensure that security settings are correctly implemented.

Run this script from the project directory using:
python security_test.py
"""

import os
import sys
import requests
from urllib.parse import urlparse
import importlib.util
import django
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
sys.path.insert(0, os.path.abspath('.'))

# Try to import Django settings
try:
    django.setup()
    from django.conf import settings
except Exception as e:
    print(f"{Fore.RED}Error loading Django settings: {e}{Style.RESET_ALL}")
    sys.exit(1)

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}\n")

def success(text):
    """Print success message."""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def warning(text):
    """Print warning message."""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def error(text):
    """Print error message."""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def check_debug_setting():
    """Check if DEBUG is set to False for production."""
    print_header("Checking DEBUG Setting")
    
    if settings.DEBUG:
        error("DEBUG is set to True. This should be False in production.")
    else:
        success("DEBUG is correctly set to False for production.")

def check_security_middleware():
    """Check if security middleware is properly configured."""
    print_header("Checking Security Middleware")
    
    required_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    for middleware in required_middleware:
        if middleware in settings.MIDDLEWARE:
            success(f"Found {middleware}")
        else:
            error(f"Missing {middleware}")
    
    # Check CSP middleware
    csp_middleware = 'csp.middleware.CSPMiddleware'
    if csp_middleware in settings.MIDDLEWARE:
        success(f"Found {csp_middleware}")
    else:
        warning(f"Consider adding {csp_middleware} for Content Security Policy")

def check_security_settings():
    """Check if security-related settings are properly configured."""
    print_header("Checking Security Settings")
    
    # Browser security headers
    if getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False):
        success("SECURE_BROWSER_XSS_FILTER is enabled")
    else:
        error("SECURE_BROWSER_XSS_FILTER should be enabled")
    
    if getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False):
        success("SECURE_CONTENT_TYPE_NOSNIFF is enabled")
    else:
        error("SECURE_CONTENT_TYPE_NOSNIFF should be enabled")
    
    if getattr(settings, 'X_FRAME_OPTIONS', '') == 'DENY':
        success("X_FRAME_OPTIONS is set to DENY")
    else:
        warning("X_FRAME_OPTIONS should be set to DENY")
    
    # Cookie security
    if getattr(settings, 'CSRF_COOKIE_SECURE', False):
        success("CSRF_COOKIE_SECURE is enabled")
    else:
        warning("CSRF_COOKIE_SECURE should be enabled in production")
    
    if getattr(settings, 'SESSION_COOKIE_SECURE', False):
        success("SESSION_COOKIE_SECURE is enabled")
    else:
        warning("SESSION_COOKIE_SECURE should be enabled in production")
    
    # HTTPS settings
    if getattr(settings, 'SECURE_SSL_REDIRECT', False):
        success("SECURE_SSL_REDIRECT is enabled")
    else:
        warning("SECURE_SSL_REDIRECT should be enabled in production")
    
    # HSTS settings
    hsts_seconds = getattr(settings, 'SECURE_HSTS_SECONDS', 0)
    if hsts_seconds > 0:
        success(f"SECURE_HSTS_SECONDS is set to {hsts_seconds}")
    else:
        warning("SECURE_HSTS_SECONDS should be set to a positive value")
    
    if getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False):
        success("SECURE_HSTS_INCLUDE_SUBDOMAINS is enabled")
    else:
        warning("SECURE_HSTS_INCLUDE_SUBDOMAINS should be enabled")
    
    if getattr(settings, 'SECURE_HSTS_PRELOAD', False):
        success("SECURE_HSTS_PRELOAD is enabled")
    else:
        warning("SECURE_HSTS_PRELOAD should be enabled")

def check_csp_settings():
    """Check if Content Security Policy is properly configured."""
    print_header("Checking Content Security Policy Settings")
    
    csp_settings = [
        'CSP_DEFAULT_SRC',
        'CSP_SCRIPT_SRC',
        'CSP_STYLE_SRC',
        'CSP_IMG_SRC',
        'CSP_FONT_SRC',
    ]
    
    for setting in csp_settings:
        if hasattr(settings, setting):
            success(f"{setting} is configured: {getattr(settings, setting)}")
        else:
            warning(f"{setting} is not configured")

def check_auth_password_validators():
    """Check if password validators are properly configured."""
    print_header("Checking Password Validators")
    
    validators = getattr(settings, 'AUTH_PASSWORD_VALIDATORS', [])
    
    if not validators:
        error("No password validators configured")
        return
    
    validator_names = [validator.get('NAME', '') for validator in validators]
    
    common_validators = [
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'django.contrib.auth.password_validation.MinimumLengthValidator',
        'django.contrib.auth.password_validation.CommonPasswordValidator',
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    ]
    
    for validator in common_validators:
        if validator in validator_names:
            success(f"Found {validator.split('.')[-1]}")
        else:
            warning(f"Missing {validator.split('.')[-1]}")

def check_template_loaders():
    """Check template loaders for security best practices."""
    print_header("Checking Template Loaders")
    
    templates = getattr(settings, 'TEMPLATES', [])
    
    for template in templates:
        if template.get('BACKEND') == 'django.template.backends.django.DjangoTemplates':
            if template.get('OPTIONS', {}).get('context_processors', []):
                success("Template context processors are configured")
            else:
                warning("Template context processors are not configured")
            
            if not template.get('APP_DIRS', True):
                warning("APP_DIRS is disabled, which might affect CSRF protection")
            else:
                success("APP_DIRS is enabled")

def check_csrf_templates():
    """Check a sample of templates for CSRF token inclusion."""
    print_header("Checking CSRF Token Usage in Templates")
    
    template_dir = os.path.join(settings.BASE_DIR, 'bookshelf', 'templates')
    if not os.path.exists(template_dir):
        error(f"Template directory not found: {template_dir}")
        return
    
    # Find form templates (likely to need CSRF protection)
    form_templates = []
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                form_templates.append(os.path.join(root, file))
    
    if not form_templates:
        warning("No templates found to check for CSRF tokens")
        return
    
    for template_path in form_templates:
        try:
            with open(template_path, 'r') as f:
                content = f.read()
                relative_path = os.path.relpath(template_path, settings.BASE_DIR)
                
                if '<form' in content:
                    if '{% csrf_token %}' in content:
                        success(f"CSRF token found in form template: {relative_path}")
                    else:
                        error(f"Form without CSRF token in: {relative_path}")
        except Exception as e:
            error(f"Error reading template {template_path}: {e}")

def main():
    """Run all security checks."""
    print_header("Django Security Test Suite")
    print(f"Testing project: {os.path.basename(settings.BASE_DIR)}")
    
    check_debug_setting()
    check_security_middleware()
    check_security_settings()
    check_csp_settings()
    check_auth_password_validators()
    check_template_loaders()
    check_csrf_templates()
    
    print_header("Security Test Complete")
    print("Review the results above to ensure your Django application is properly secured.")
    print("Remember that this is a basic check and does not replace a comprehensive security audit.")

if __name__ == "__main__":
    main()