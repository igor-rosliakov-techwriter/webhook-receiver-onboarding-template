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

### Responsibility boundary

Signature generation is the responsibility of the webhook sender
(webhook provider), not this service.

The webhook receiver **never generates signatures** in production.
Its only responsibility is to verify signatures on incoming requests.

For local development and onboarding purposes, this repository includes
helper tooling to simulate a webhook provider.


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

For local testing, this is why the Makefile and helper script always
sign the payload file using its raw byte representation and send it
using `--data-binary`.


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

For local development and onboarding, this repository includes helper
tooling to simulate a webhook provider.

### Recommended approach

The recommended way to send a signed webhook request locally is to use
the provided Makefile:

```bash
make send
```

This command:
- Generates a valid HMAC-SHA256 signature using the shared secret from `.env`.
- Signs the exact raw request body bytes.
- Sends a sample webhook payload to the local service.

This approach avoids common pitfalls related to shell quoting and
payload formatting and ensures consistent signature verification.

### Helper script

Internally, `make send` uses a small helper script:

[scripts/sign_payload.py](https://github.com/igor-rosliakov-techwriter/webhook-receiver-onboarding-template/blob/main/scripts/sign_payload.py)


This script reads the payload file as raw bytes and computes an HMAC
signature using the shared secret from the environment.

It exists solely to support local testing and onboarding and is not
part of the production request flow.
