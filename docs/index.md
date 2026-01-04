# Documentation Index

This documentation set is organized as an onboarding template for a minimal webhook receiver.

## Start here (new engineer)

- Onboarding overview: [`onboarding/00-overview.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/00-overview.md)
- Local setup: [`onboarding/01-local-setup.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/01-local-setup.md)
- First task: [`onboarding/02-first-task.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/02-first-task.md)
- Common pitfalls: [`onboarding/03-common-pitfalls.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/03-common-pitfalls.md)

## Architecture

These documents explain how the service works internally
and are useful once you understand the basic onboarding flow.

- System overview and webhook flow: [`architecture/overview.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/architecture/overview.md).
- Security model (signatures, secrets): [`architecture/security.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/architecture/security.md).
- Event lifecycle (receive → validate → dedupe → dispatch): [`architecture/event-lifecycle.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/architecture/event-lifecycle.md).

## Operations

Operational documents are intended for troubleshooting
once the service is running or integrated.

- Troubleshooting runbook: [`runbook/troubleshooting.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/runbook/troubleshooting.md).

## Decisions

- ADR-0001 — Idempotency: [`adr/0001-idempotency.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/adr/0001-idempotency.md).

## Reference

- Glossary: [`glossary.md`](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/glossary.md).
