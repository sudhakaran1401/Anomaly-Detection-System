# Security Testing

## Automated scope
- Authentication and protected endpoints
- Cross-user resource isolation
- Path traversal filenames
- Unsupported upload content types
- File-size limits
- CSV header validation
- Download path containment
- Security configuration

## Manual/deployment checks
- `python manage.py check --deploy`
- HTTPS and secure cookies
- Production secret management
- Browser session/logout behavior
- XSS review of user-controlled output

## Status
Automated security tests are implemented. Runtime status must be recorded from the actual environment.
