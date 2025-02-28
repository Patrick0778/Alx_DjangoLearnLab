# Library Project - Secure Django Application

This Django project implements comprehensive security measures to protect against common web vulnerabilities.

## Security Features Implemented

### 1. Secure Settings Configuration

- Debug mode is disabled in production
- HTTPS enforcement through SSL redirects and HSTS
- Secure cookie configuration
- Browser security headers (XSS protection, content type, X-Frame-Options)
- Content Security Policy implementation

### 2. CSRF Protection

- All forms are protected with Django's CSRF token mechanism
- CSRF middleware is properly configured

### 3. Secure Data Handling

- Input validation and sanitization
- HTML escaping to prevent XSS attacks
- Django's ORM used for parameterized queries (preventing SQL injection)

### 4. Authentication & Authorization

- Strong password policies enforced
- Role-based access control
- Proper permission checks on views
- Protection for sensitive parameters

### 5. Content Security Policy

- CSP headers configured to restrict content loading

## Getting Started

### Prerequisites

- Python 3.8+
- Django 5.1+

### Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

### Security Testing

Run the security test script to verify security configurations:

```bash
python security_test.py
```

## Security Documentation

For detailed information about the security measures implemented, see [SECURITY.md](SECURITY.md).

## Project Structure

- `LibraryProject/` - Core settings and configuration
- `bookshelf/` - Main application, contains models, views, templates
- `security_test.py` - Script to validate security configurations
- `SECURITY.md` - Detailed security documentation

## Best Practices for Development

1. Always validate user inputs
2. Use Django forms for input handling
3. Include CSRF tokens in all forms
4. Keep dependencies updated
5. Follow the principle of least privilege
