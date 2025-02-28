# LibraryProject Security Documentation

This document outlines the security measures implemented in the LibraryProject application.

## Production Security Settings

The application uses the following security-focused settings in `settings.py`:

- `DEBUG = False` in production to prevent leakage of sensitive debugging information
- `SECURE_BROWSER_XSS_FILTER = True` to enable browser XSS filtering
- `SECURE_CONTENT_TYPE_NOSNIFF = True` to prevent MIME-type sniffing
- `X_FRAME_OPTIONS = 'DENY'` to prevent clickjacking attacks by denying framing
- `CSRF_COOKIE_SECURE = True` to send CSRF cookies only over HTTPS
- `SESSION_COOKIE_SECURE = True` to send session cookies only over HTTPS
- `SECURE_SSL_REDIRECT = True` to redirect HTTP to HTTPS
- `SECURE_HSTS_SECONDS = 31536000` (1 year) for HTTP Strict Transport Security
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True` to include all subdomains in HSTS
- `SECURE_HSTS_PRELOAD = True` to make the site eligible for HSTS preloading

## Content Security Policy

CSP headers are configured to restrict the sources from which content can be loaded, helping to prevent XSS attacks:

```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'",)
```

The `django-csp` middleware is included in the middleware stack.

## CSRF Protection

All forms in the application use Django's built-in CSRF protection with the `{% csrf_token %}` template tag.
The `CsrfViewMiddleware` is enabled in the middleware configuration.

## Input Validation and Sanitization

User inputs are validated and sanitized to prevent injection attacks:

- Form inputs are validated using Django's form validation system
- HTML content is escaped using `django.utils.html.escape()`
- Strong password policies are enforced (minimum length, character requirements)

## Authentication and Authorization

The application implements:

- Role-based access control (Admin, Librarian, Member)
- Per-view permission checks using decorators like `@permission_required`
- Protection of sensitive POST parameters with `@sensitive_post_parameters`
- Secure password handling with Django's password hashing

## Exception Handling

Exceptions are caught and handled properly to prevent information leakage:

- Generic error messages are shown to users
- Detailed errors are not exposed in production

## Security Testing Checklist

- [x] Verify DEBUG is set to False in production
- [x] Confirm all forms include CSRF tokens
- [x] Test for SQL injection vulnerabilities
- [x] Validate XSS protection in user inputs
- [x] Check authorization controls for different user roles
- [x] Verify HTTPS enforcement
- [x] Test password policy enforcement
- [x] Validate Content Security Policy effectiveness

## Best Practices for Developers

1. Always validate and sanitize user inputs
2. Use Django's ORM for database queries instead of raw SQL
3. Include CSRF tokens in all forms
4. Apply the principle of least privilege when assigning permissions
5. Use Django's built-in authentication system
6. Keep dependencies updated to avoid security vulnerabilities
7. Use proper exception handling to prevent information disclosure
