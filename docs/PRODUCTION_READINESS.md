# Production Readiness Checklist

This repository is a DevOps portfolio and must not be treated as a production control plane until every required control below is implemented, verified, and recorded.

## Release controls

- [ ] Protect `main`: require pull requests, passing checks, and no force pushes.
- [ ] Disable unrestricted automatic approval and merge for production-bound changes.
- [ ] Require CI to pass before merge.
- [ ] Require an explicit approval before production promotion.
- [ ] Record the commit SHA, artifact digest, environment, approver, and deployment result for every release.
- [ ] Maintain a tested rollback procedure to the last known healthy deployment.

## Security controls

- [ ] Store secrets in an approved secret manager; never commit secrets to the repository.
- [ ] Enable repository secret scanning, push protection, dependency alerts, and code scanning.
- [ ] Use least-privilege CI credentials and short-lived identity tokens where supported.
- [ ] Pin third-party GitHub Actions to reviewed commits or approved versions.
- [ ] Review Terraform, Kubernetes, Docker, and workflow changes through pull requests.
- [ ] Define data classification, retention, access review, and incident-response procedures.

## Environment controls

- [ ] Maintain isolated development, staging, and production environments.
- [ ] Deploy to staging automatically and run health, smoke, and integration tests.
- [ ] Promote only a verified artifact from staging to production.
- [ ] Configure backups, restoration tests, service ownership, and recovery objectives.
- [ ] Configure rate limits, retry limits, dead-letter handling, and idempotency for automation workflows.

## Observability controls

- [ ] Emit structured application and workflow logs without secrets or customer-sensitive data.
- [ ] Monitor availability, latency, error rate, throughput, queue depth, costs, and security events.
- [ ] Define alert thresholds and an escalation owner for each critical service.
- [ ] Test an incident workflow, including diagnosis, containment, rollback, and post-incident review.

## External-action controls

- [ ] Require explicit approval for production deployments, billing/refunds, contracts, purchases, access changes, data deletion, and outbound campaigns.
- [ ] Use consent, opt-out, rate-limit, and suppression controls for sales or marketing messages.
- [ ] Verify payment webhook signatures and make customer provisioning idempotent.
- [ ] Maintain an immutable audit record for every autonomous workflow execution.

## Go-live evidence

A production launch requires documented evidence that all applicable controls above are complete, an end-to-end staging run has passed, and a rollback drill has succeeded.
