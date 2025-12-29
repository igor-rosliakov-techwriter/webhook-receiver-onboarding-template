# Event lifecycle

This document explains how a webhook event moves through the system
from initial receipt to final acknowledgment.

## Overview

Webhook providers may deliver the same event multiple times,
and delivery order is not always guaranteed.
The service must therefore treat each incoming request carefully.

## Event processing lifecycle

An incoming webhook event goes through the following stages:

1. **Receive raw request**
   - Accept the HTTP `POST /webhooks` request
   - Read the raw request body bytes

2. **Verify signature**
   - Read the `X-Signature` header
   - Compute the expected HMAC signature using `WEBHOOK_SECRET`
   - Reject the request with `401 Unauthorized` if verification fails

3. **Parse JSON payload**
   - Decode the request body
   - Parse JSON payload
   - Reject invalid JSON with `400 Bad Request`

4. **Validate event identifier**
   - Extract `event_id` from the payload
   - Reject requests without a valid event identifier

5. **Idempotency check**
   - Check whether the `event_id` has already been processed
   - If the event is a duplicate:
     - skip further processing
     - return a successful response

6. **Handle / dispatch event**
   - Perform minimal event handling based on `event_type`
   - (In this template, business logic is intentionally minimal)

7. **Respond**
   - Return a `200 OK` response to acknowledge receipt

## Duplicate delivery behavior

If a webhook event with the same `event_id` is delivered more than once,
the service does not process it again.

Instead, it:
- logs the duplicate delivery
- returns a `200 OK` response with `status: duplicate`

Returning a successful response prevents the webhook provider
from retrying the same event indefinitely.

## Notes

- The service responds as early as possible to prevent unnecessary retries
  from the webhook provider.
- Idempotency checks are performed before any business logic.
- Heavy or asynchronous processing should not block the request-response cycle.
