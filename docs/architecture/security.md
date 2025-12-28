# Security: webhook signature verification

This document describes how incoming webhook requests are authenticated
and how forged or tampered requests are rejected.

The webhook receiver exposes a public HTTP endpoint (`POST /webhooks`).
Without additional verification, any third party could send requests to it.
To prevent this, each request must include a cryptographic signature.

---

## Security goals

The primary security goals of the webhook receiver are:

- ensure that incoming requests originate from a trusted sender
- ensure that request payloads have not been modified in transit
- reject unauthenticated or malformed requests as early as possible

---

## Threat model (simplified)

The following threats are considered in scope for this service:

- forged webhook requests sent by third parties
- accidental requests from the wrong environment (e.g. staging to production)
- modified payloads sent without knowledge of the shared secret

The following threats are **out of scope** for this template and documented
as future improvements:

- replay attacks using previously valid requests
- denial-of-service attacks

---

## Approach: HMAC-SHA256 with a shared secret

The service uses an HMAC-based signature to authenticate webhook requests.

A shared secret (`WEBHOOK_SECRET`) is known to:
- the webhook sender (provider)
- this webhook receiver service

For each request, the sender computes an HMAC-SHA256 signature over the
**raw request body bytes** and includes it in an HTTP header.
The service recomputes the signature and compares it with the received value.

---

## Signature format

### Header name
```
X-Signature
```
### Header value format
```
sha256=<hex_digest>
```
### Example
```
X-Signature: sha256=a94f2e9c0f3b6e2c...
```


---

## What is signed (important)

The signature is computed over the **raw request body bytes**.

On the service side, this corresponds to:

- using `request.body()` (raw bytes)
- **not** re-serializing parsed JSON

### Why raw body is used

JSON can be serialized in multiple valid ways (different key order,
whitespace, or formatting). Re-serializing JSON may produce a different
byte sequence and cause signature verification to fail.

Using the raw request body guarantees that both sender and receiver
sign the exact same data.

---

## Verification flow (service side)

For each incoming webhook request, the service performs the following steps:

1. Read the raw request body bytes.
2. Read the `X-Signature` header.
3. Compute an HMAC-SHA256 signature using `WEBHOOK_SECRET` and the raw body.
4. Format the computed signature as `sha256=<hex_digest>`.
5. Compare the computed signature with the received one using a
   constant-time comparison.
6. If the signature is missing or invalid, return `401 Unauthorized`.

---

## Failure modes

| Scenario                        | Response |
|--------------------------------|----------|
| Missing `X-Signature` header   | `401 Unauthorized` |
| Invalid signature              | `401 Unauthorized` |
| Invalid JSON payload           | `400 Bad Request` |

---

## Configuration

The shared secret is provided via environment variables.

```env
WEBHOOK_SECRET=<secret value>
```


The secret must not be hardcoded or committed to version control.
For local development, it can be defined in a `.env` file.

---

## Local development example

To compute a valid signature for a local request:

```bash
SECRET="dev_secret_123"
BODY="$(cat examples/payloads/payment_succeeded.json)"
SIG=$(printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')
echo "sha256=$SIG"
```

Send the request with the computed signature:

```bash
curl -X POST "http://localhost:8000/webhooks" \
  -H "Content-Type: application/json" \
  -H "X-Signature: sha256=$SIG" \
  --data-binary @examples/payloads/payment_succeeded.json
```


