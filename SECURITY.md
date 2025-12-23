# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

## Security Best Practices

### Infrastructure
- Never commit secrets or credentials
- Use AWS Secrets Manager or HashiCorp Vault
- Enable MFA for all cloud accounts
- Implement least privilege access
- Regular security audits and compliance checks

### Containers
- Scan images for vulnerabilities
- Use minimal base images
- Run containers as non-root
- Implement network policies

### CI/CD
- Use encrypted secrets in pipelines
- Implement security scanning stages
- Sign and verify container images
- Audit pipeline access logs

## Reporting a Vulnerability

Email: security@garrettcarroll.dev

**Do not open public issues for security vulnerabilities.**

Response time: 48 hours

Thank you for helping keep this infrastructure secure!
