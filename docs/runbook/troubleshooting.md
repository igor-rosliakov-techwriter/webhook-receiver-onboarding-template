# Troubleshooting runbook

This runbook provides operational guidance for diagnosing and handling
common issues related to webhook processing.

## Purpose

Webhook receivers operate at the boundary between external providers
and internal systems. Failures are often caused by misconfiguration,
payload mismatches, or retry behavior.

This document helps quickly identify whether an issue is:
- a client-side integration problem
- an expected webhook retry scenario
- a receiver misconfiguration

## How this runbook should be used

This runbook is intended for:
- on-call engineers
- developers debugging webhook integrations
- team members responding to delivery issues

Each scenario includes:
- observable symptoms
- likely causes
- how to confirm the issue
- recommended actions

---

## Invalid or malformed JSON (400 Bad Request)

### Symptom
- HTTP `400 Bad Request`
- Response indicates invalid JSON payload

### Likely causes
- Malformed JSON (missing commas, brackets, quotes)
- Payload truncated or manually edited
- Incorrect `Content-Type` header

### How to confirm
Send a known invalid payload manually using `curl` or the HTTP example file.

Check server logs for JSON parsing errors.

### Recommended action
- Validate payload JSON before sending
- Ensure the payload file is sent as raw bytes
- Use example payloads from `examples/payloads/`

---

## Invalid signature (401 Unauthorized)

### Symptom
- HTTP `401 Unauthorized`
- Response body indicates `invalid_signature`

### Likely causes
- Missing `X-Signature` header
- Signature computed using a different secret
- Signature computed over modified payload bytes

### How to confirm
Compare:
- `WEBHOOK_SECRET` in the receiver
- secret used by the signing script
- raw payload bytes sent to the server

### Recommended action
Use the provided Makefile to send requests:

```bash
make send PAYLOAD=examples/payloads/payment_succeeded.json
```

This ensures correct signing and payload integrity.

---

## Duplicate webhook events

### Symptom

- HTTP `200 OK`
- Response body:

```json
{ "status": "duplicate" }
```

### Likely cause

Webhook providers may retry delivery when:
- network timeouts occur;
- responses are delayed;
- acknowledgements are not received.
 
### How to confirm

Send the same payload twice with the same event_id.
Check logs for duplicate detection.

### Recommended action

No action required. Duplicate detection and idempotency 
are expected behaviors and prevent double-processing of events.

---

## Retry storms or repeated deliveries

### Symptom

- The same event is received many times in a short period.
- Logs show repeated requests with identical event_id.

### Likely cause

The webhook provider retries aggressively due to:
- previous non-2xx responses;
- slow acknowledgements;
- temporary network failures.

### How to confirm

Check response codes and response times in logs.

### Recommended action

- Ensure the receiver responds quickly.
- Return 200 OK for successfully received events.
- Verify idempotency checks occur before business logic.

---

## Slow responses or timeouts

### Symptom

- Webhook provider reports timeouts.
- Receiver logs show long processing times.

### Likely causes

- Heavy logic inside webhook handlers.
- Blocking operations (I/O, sleep, external calls).

### Recommended action

- Keep webhook handlers lightweight.
- Offload heavy processing to background workers.
- Acknowledge webhook delivery as early as possible.
