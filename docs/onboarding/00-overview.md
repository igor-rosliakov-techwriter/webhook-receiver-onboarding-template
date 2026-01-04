# Onboarding overview

## What this service does

This service receives webhook events from an external provider and returns a stable HTTP response.

Typical responsibilities of a webhook receiver:
- validate authenticity (signatures / shared secrets)
- handle retries and duplicate deliveries (idempotency)
- keep request processing fast (avoid long synchronous work)
- provide observability (logs and clear error patterns)

## What you will do during onboarding

1) Run the service locally ([docs/onboarding/01-local-setup.md - Local setup]([docs/onboarding/01-local-setup.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/01-local-setup.md)))
2) Send a sample webhook request ([docs/onboarding/01-local-setup.md - Send a signed webhook request](([docs/onboarding/01-local-setup.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/01-local-setup.md))))
3) Implement support for a new event type ([docs/onboarding/02-first-task.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/02-first-task.md))
4) Learn common pitfalls and troubleshooting patterns ([docs/onboarding/03-common-pitfalls.md](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/docs/onboarding/03-common-pitfalls.md))
