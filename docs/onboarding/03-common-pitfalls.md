# Common pitfalls

This document highlights common issues encountered when developing
and testing webhook receivers, along with recommended solutions.

---

## 401 Unauthorized: invalid signature

A `401 Unauthorized` response indicates that signature verification failed.

### Common causes

- **Missing signature header**  
  The `X-Signature` header is not included in the request.

- **Signature computed with a different secret**  
  The signing secret does not match `WEBHOOK_SECRET` configured
  in the receiver.

- **Payload bytes do not match**  
  The signature was computed over different bytes than those sent.

  This often happens when:
  - signing inline JSON instead of a file
  - modifying whitespace or formatting
  - using `curl -d` instead of `--data-binary`

### How to fix quickly

For local development, always use:

```bash
make send PAYLOAD=examples/payloads/payment_succeeded.json
```

This ensures:
- correct secret usage;
- signing of raw payload bytes;
- identical bytes sent to the server.

## Address already in use (Errno 48)

### Symptom

Server fails to start with:
```css
Address already in use
```

### Cause

Another instance of the webhook receiver is already running.

This usually happens when:
- the server is started twice;
- make run is executed in multple terminals;

### How to fix

- Keep the server running in one terminal:
```bash
make run
```

- Send requests from a separate terminal:
```bash
make send
```

- Stop the existing process before restarting.

## Duplicate deliveries

Webhook providers may deliver the same event multiple times due to:
- retries
- timeouts
- network instability

### Expected behavior

When the same event_id is received more than once:
- the event is not processed again;
- the receiver responds with `200 OK`;
- the response includes:
```json
{ "status": "duplicate" }
```

This is intentional and prevents infinite retries.

## Ignored event types

If an unknown event_type is received:
- the event is acknowledged with `200 OK`;
- no handler is executed;
- the event is logged as ignored.

This prevents unnecessary retries for unsupported event types.

## General recommendations

- Never log secrets or raw signature values.
- Keep webhook handlers lightweight.
- Perform idempotency checks before business logic.
- Always acknowledge valid deliveries quickly.
