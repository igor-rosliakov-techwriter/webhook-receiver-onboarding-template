# First task: add a new event type

This guide walks you through your first practical task in this project:
**adding support for a new webhook event type**.

You will:
- add a new handler
- register it in the dispatcher
- send a test webhook locally
- verify the expected behavior

The example below uses the `subscription_created` event.

---

## Goal

Add support for a new webhook event type (`subscription_created`) and verify that it is:
- correctly dispatched
- handled exactly once
- safely ignored if unknown
- protected by signature verification and idempotency

---

## Prerequisites

Before starting, make sure:

- the service is running locally:
  ```bash
  make run
  ```

- the environment is configured:
`.env` exists
`WEBHOOK_SECRET` is set

## Where to make changes

You will touch the following files:

| File                  | Purpose                              |
| --------------------- |:------------------------------------:|
| `src/handlers.py`     | Add a new event handler              |
| `src/dispatch.py`     | Register the handler by `event_type` |
| `examples/payloads/`  | Add a sample webhook payload         |

No changes to the webhook endpoint or Makefile are required.

## Step 1: Create a sample payload

Create a new file:
  ```bash
examples/payloads/subscription_created.json
  ```

  ```json
{
  "id": "evt_003",
  "type": "subscription_created",
  "data": {
    "subscription_id": "sub_123",
    "user_id": "user_456",
    "plan": "pro_monthly",
    "started_at": "2025-12-31T00:00:00Z"
  }
}
  ```

This payload simulates a typical webhook sent by a billing or subscription system.

## Step 2: Add a handler

Open `src/handlers.py` and add a new handler function:

  ```python
def handle_subscription_created(payload: dict, logger, request_id: str) -> None:
    event_id = payload.get("id") or payload.get("event_id")
    data = payload.get("data") or {}

    subscription_id = data.get("subscription_id")
    user_id = data.get("user_id")
    plan = data.get("plan")

    logger.info(
        "handler_subscription_created request_id=%s event_id=%s subscription_id=%s user_id=%s plan=%s",
        request_id,
        event_id,
        subscription_id,
        user_id,
        plan,
    )
  ```

The handler intentionally contains no business logic.
Its purpose is to show where domain-specific processing would be implemented.

## Step 3: Register the handler in the dispatcher

Open `src/dispatch.py`.

1. Import the new handler:
  ```python
from .handlers import handle_subscription_created
  ```

2. Register it in the handler registry:
  ```python
HANDLERS = {
    "payment_succeeded": handle_payment_succeeded,
    "subscription_created": handle_subscription_created,
}
  ```

The dispatcher uses this mapping to route incoming events by `event_type`.

## Step 4: Send the webhook locally

Use the existing Makefile command and override the payload path:
  
  ```bash
make send PAYLOAD=examples/payloads/subscription_created.json
  ```

This command:
- computes the correct HMAC signature.
- sends the raw request body.
- calls the /webhooks endpoint.

## Step 5: Verify the result

### Expected HTTP response

  ```json
{
  "request_id": "...",
  "status": "ok",
  "event_id": "evt_003",
  "event_type": "subscription_created"
}
  ```

## Expected logs

### You should see a handler-specific log entry:

  ```bash
handler_subscription_created request_id=... event_id=evt_003 subscription_id=sub_123 user_id=user_456 plan=pro_monthly
  ```

This confirms that:
- the dispatcher matched the event type
- the handler was executed
- the request completed successfully

### Idempotency check (recommended)

Send the same payload again:

  ```bash
make send PAYLOAD=examples/payloads/subscription_created.json
  ```

Expected behavior:
- HTTP response: `status: duplicate`
- no handler log is emitted
  
Duplicate deliveries are acknowledged but not processed again.

### Unknown event types

If an event type is not registered in the dispatcher, it is safely ignored.

Example:

  ```bash
make send PAYLOAD=examples/payloads/unknown_event.json
  ```

Expected behavior:
- HTTP 200
- `status: ignored`
- no handler execution
  
This prevents unnecessary retries from external providers.

### Common pitfalls

- Typos in handler names or dispatcher registry.
- Forgetting to register the handler in HANDLERS.
- Reusing the same event_id during testing (triggers idempotency).
- Computing the signature from parsed JSON instead of the raw request body.

## Summary

You have:

- added a new event handler.
- registered it in the dispatcher.
- tested it locally with a signed webhook.
- verified idempotency and unknown-event behavior.
  
This is the standard workflow for extending the webhook receiver with new event types.
