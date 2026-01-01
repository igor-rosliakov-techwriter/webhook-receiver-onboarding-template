# Event lifecycle

This document describes how an incoming webhook request is processed by the service,
from initial receipt to final acknowledgment. The focus is on correctness, safety, 
and predictable behavior in the presence of retries, duplicates, and unknown event types.

---

## Overview

Webhook providers typically use at-least-once delivery:
the same event may be delivered multiple times,
and delivery order is not guaranteed.

The service must therefore:
- verify authenticity of incoming requests;
- handle duplicate deliveries safely;
- avoid triggering unnecessary retries;
- remain extensible as new event types are added.

---

## Event processing lifecycle

Each incoming webhook request goes through the following stages:

### 1. Receive raw request

- Accept the HTTP `POST /webhooks` request.
- Read the raw request body bytes.
- Do not modify or parse the body at this stage.

The raw body is required for correct signature verification.

---

### 2. Verify signature

- Read the `X-Signature` header.
- Compute the expected HMAC-SHA256 signature using `WEBHOOK_SECRET`.
- Compare signatures using a constant-time comparison.

If verification fails:
- the request is rejected with `401 Unauthorized`;
- no further processing is performed.

---

### 3. Parse JSON payload

- Decode the request body.
- Parse the JSON payload.

If the payload is not valid JSON:
- the request is rejected with `400 Bad Request`.

---

### 4. Validate event identifier

- Extract the event identifier (`id` / `event_id`) from the payload.

If no valid event identifier is present:
- the request is rejected with `400 Bad Request`.

The event identifier is required for idempotency handling.

---

### 5. Idempotency check

- Check whether the `event_id` has already been processed.

If the event is a duplicate:
- further processing is skipped;
- the service immediately returns a successful response;
- the duplicate delivery is logged.

This prevents duplicate side effects and unnecessary retries
from the webhook provider.

---

### 6. Dispatch by event type

- Extract the `event_type` from the payload.
- Route the event to a registered handler using a dispatcher.

If a matching handler exists:
- the handler is executed;
- the event is considered successfully processed.

If the event type is unknown:
- the event is safely ignored;
- no handler is executed;
- the request is still acknowledged successfully.

This behavior allows the service to accept new or unsupported
event types without causing retry storms.

---

### 7. Respond to the provider

- Return a `200 OK` response with a processing status:
  - `ok` — handler executed;
  - `duplicate` — event already processed;
  - `ignored` — unknown event type.

Returning a successful response signals to the provider
that the event has been received and does not need to be retried.

---

## Duplicate delivery behavior

When the same `event_id` is delivered more than once,
the service guarantees *exactly-once processing semantics* at the handler level.

Duplicate requests:
- are acknowledged with `200 OK`;
- do not trigger handler execution;
- are logged for observability.

---

## Design notes

- The service responds as early as possible to minimize retries.
- Idempotency checks are performed before any handler logic.
- Unknown event types are acknowledged but ignored.
- Heavy or asynchronous processing should be delegated to background workers
  and must not block the request-response cycle.

This lifecycle is intentionally simple and explicit,
making the system easy to reason about and extend.
