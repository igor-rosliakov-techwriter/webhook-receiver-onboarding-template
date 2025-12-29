# Webhook Receiver — Onboarding Documentation Template

This repository is a **portfolio project** focused on backend onboarding documentation.

It uses a minimal webhook receiver as an example service to demonstrate how onboarding guides,
architecture docs, runbooks, and ADRs can be structured in a real-world backend team.

> Note: The code is intentionally minimal and exists to support the documentation.
> This is not a production-ready service.

## What’s inside

- **Onboarding docs**:
  - overview
  - local setup
  - first task
  - common pitfalls
- **Architecture docs**:
  - request flow
  - security notes
  - event lifecycle
- **Runbook**: troubleshooting scenarios and operational guidance
- **ADR**:
  - key design decision(s), e.g. idempotency
- **Examples**:
  - sample payloads
  - example requests
  - example responses
- **Diagram**: webhook processing flow

## Documentation map

Start here: [docs/index.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/index.md)

Suggested reading order for onboarding:
1) [docs/onboarding/00-overview.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/00-overview.md)
2) [docs/onboarding/01-local-setup.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/01-local-setup.md)
3) [docs/onboarding/02-first-task.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/02-first-task.md)
4) [docs/onboarding/03-common-pitfalls.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/03-common-pitfalls.md)

## Scope

Implemented (minimal):
- HTTP endpoint to receive webhook requests
- Documentation-first repository structure

Planned / documented:
- signature verification (HMAC)
- idempotency and duplicate delivery handling
- event dispatching and error patterns
- operational troubleshooting

## How to use this repo

- As an onboarding template example (structure + writing style)
- As a reference for documenting backend services:
  - security assumptions
  - lifecycle diagrams
  - runbooks and ADRs
 
## Quick start

This repository includes a small Makefile to simplify local setup and testing.

### 1. Environment setup

```bash
python -m venv .venv
source .venv/bin/activate
make setup
cp .env.example .env
```

Edit .env and set your own value for WEBHOOK_SECRET.

### 2. Run the service (Terminal 1)

Start the webhook receiver locally:

```bash
make run
```

The service will start listening on http://localhost:8000.
> Note: This command runs a long-lived server process and will keep the terminal busy.

### 3. Send a signed webhook request (Terminal 2)

Open a second terminal window in the same repository and run:

```bash
make send
```

This command:
- generates a valid request signature using the shared secret from .env
- sends a sample webhook payload to the local service

You should receive a `200 OK` response.
Sending the same request again will return `status: duplicate`.

For a detailed explanation of the local setup and testing workflow, see:
- [docs/onboarding/01-local-setup.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/01-local-setup.md)
- [docs/index.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/index.md)
