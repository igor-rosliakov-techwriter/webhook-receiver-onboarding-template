# Common pitfalls

This document highlights common issues encountered when developing
and testing webhook receivers, along with recommended solutions.

---

## 401 Unauthorized: invalid signature

A `401 Unauthorized` response indicates that the webhook signature
verification has failed.

### Common causes

- **Missing signature header**  
  The `X-Signature` header is not included in the request.

- **Signature computed with a different secret**  
  The secret used to generate the signature does not match
  `WEBHOOK_SECRET` configured in the receiver.

- **Payload bytes do not match**  
  The signature is computed over a different byte representation
  than the one sent to the server.

  This often happens when:
  - signing inline JSON instead of a file
  - modifying whitespace or formatting
  - using `curl -d` instead of `--data-binary`

### Recommended solution

For local development, use the provided Makefile:

```bash
make send
```

This ensures that:
- The signature is generated using the correct secret.
- The exact raw payload bytes are signed.
- The same bytes are sent to the server.

## Address already in use (Errno 48)

You may encounter an error like:

```
Address already in use
```

### Cause
The webhook receiver is already running and listening on the same port.
This commonly happens when:

- The server is started twice.
- Make run is executed while an existing instance is still running.

### Solution

- Keep the server running in one terminal:
```
make run
```

- Send requests from a separate terminal:
```
make send
```

- Stop the existing process before restarting the server.

## Duplicate deliveries

Webhook providers may deliver the same event multiple times due to:
- network timeouts
- slow responses
- non-2xx HTTP responses
This behavior is expected and must be handled explicitly.

### Expected behavior

When the same event_id is received more than once:
- the service detects the duplicate
- the event is not processed again
- a `200 OK` response is returned with:
```json
{
  "status": "duplicate"
}
```

Returning a successful response prevents the provider from retrying
the same event indefinitely.

## Additional notes

- Avoid logging secrets or signature values.
- Keep webhook handlers lightweight and return responses quickly.
- Perform idempotency checks before any business logic.
