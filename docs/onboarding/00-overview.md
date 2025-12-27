# Onboarding overview

## What this service does

This service receives webhook events from an external provider and returns a stable HTTP response.

Typical responsibilities of a webhook receiver:
- validate authenticity (signatures / shared secrets)
- handle retries and duplicate deliveries (idempotency)
- keep request processing fast (avoid long synchronous work)
- provide observability (logs and clear error patterns)

## What you will do during onboarding

1) Run the service locally
2) Send a sample webhook request
3) Implement support for a new event type
4) Learn common pitfalls and troubleshooting patterns
