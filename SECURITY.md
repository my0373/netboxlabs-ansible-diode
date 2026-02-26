# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, please email [my0373@gmail.com](mailto:my0373@gmail.com) with:

- A description of the vulnerability
- Steps to reproduce it
- The potential impact
- Any suggested fixes (optional)

You should receive a response within 48 hours acknowledging the report. We will work with you to understand the issue and coordinate a fix before any public disclosure.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |

## Security Best Practices

When using this collection:

- **Never commit credentials** to version control. Use Ansible Vault, environment variables, or a secrets manager.
- **Use TLS** (`grpcs://`) for all production Diode connections.
- **Avoid `skip_tls_verify: true`** in production environments.
- The `client_secret` parameter is marked `no_log: true` and will not appear in Ansible output or logs.
