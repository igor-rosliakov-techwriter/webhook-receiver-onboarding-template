# Glossary

This glossary explains key terms used in this repository and in webhook-based backend systems.
Definitions are written with onboarding in mind and assume no prior deep backend experience.

---

## Webhook

HTTP callback sent by one system (the provider)
to notify another system (the receiver) that an event has occurred.

Unlike APIs that are called by clients on demand,
webhooks are **pushed** by the provider when something happens.

Example:
- a payment is completed
- a user is created
- a repository is updated

The provider sends an HTTP request (usually POST) to a predefined URL.

---

## Webhook provider

System that sends webhook events.

Examples include payment systems, version control platforms,
or third-party services that notify external systems about changes.

Important characteristics:
- the provider controls when events are sent
- the provider retries delivery if it believes the event was not received
- the provider does not have direct visibility into the receiver’s internal state

---

## Webhook receiver

System that accepts incoming webhook requests.

Its responsibilities typically include:
- accepting HTTP requests
- validating request structure
- verifying authenticity (signatures)
- handling duplicate deliveries
- triggering internal processing
- returning a stable HTTP response

The receiver must be prepared to handle unreliable delivery conditions.

---

## Event

Represents something that happened in the provider’s system.

Events are usually immutable facts, for example:
- “payment succeeded”
- “invoice failed”
- “user was deleted”

An event is typically represented as a JSON object
and includes an identifier, a type, and associated data.

---

## Event type

Describes the kind of event that occurred.

Examples:
- `payment_succeeded`
- `payment_failed`
- `user_created`

Event types are commonly used to:
- route events to specific handlers
- apply different business logic
- document supported behaviors

---

## Event ID

Unique identifier assigned to an event by the provider.

It is critical for:
- detecting duplicate deliveries
- implementing idempotency
- correlating logs and debugging issues

A stable event ID allows the receiver to recognize
that multiple requests represent the same logical event.

---

## Delivery

Single attempt by the provider
to send an event to the receiver.

Important distinction:
- one event may result in multiple deliveries
- deliveries may succeed or fail independently

Each delivery is a technical attempt, not a new event.

---

## Retry

Occurs when the provider attempts to deliver
the same event again after a failure or timeout.

Retries may happen when:
- the receiver does not respond
- the receiver responds too slowly
- the receiver responds with a non-2xx HTTP status code

Retries are expected behavior in webhook systems.

---

## Duplicate delivery

Repeated delivery of the same event (same event ID).

Duplicate deliveries are normal and should not be treated as errors.

Webhook receivers must assume that any event
may be delivered more than once.

---

## Idempotency

Property of an operation that allows it to be performed multiple times
without changing the final result after the first successful execution.

In webhook processing, idempotency means:
- processing the same event once or multiple times
  leads to the same system state

Idempotency is essential to prevent duplicated side effects.

---

## Side effect

Any change to system state that occurs as a result of processing an event.

Examples:
- charging a payment
- creating an order
- sending an email
- updating a database record

Side effects must be protected from being applied multiple times
when duplicate deliveries occur.

---

## Idempotency store

Storage mechanism used to track which events have already been processed.

Its purpose is to:
- record processed event IDs
- detect duplicate deliveries
- prevent repeated side effects

In this project, the idempotency store is planned
to be implemented in memory for demonstration purposes.
Production systems typically use external storage.

---

## HMAC (Hash-based Message Authentication Code)

Cryptographic mechanism used to verify that a message has 
not been altered and was sent by a trusted party.

Webhook providers often compute an HMAC signature
using a shared secret and the raw request body.

The receiver recomputes the signature
and compares it with the value sent by the provider.

---

## Signature

Cryptographic value included in a webhook request to prove authenticity.

It is usually sent in an HTTP header
and derived from:
- the raw request body
- a shared secret

Invalid signatures indicate that the request
should not be trusted.

---

## Shared secret

Value known only to the provider and the receiver.

It is used as input to signature computation
and must be kept confidential.

Shared secrets should:
- never be committed to source control
- be provided via environment variables or secret managers

---

## Raw request body

The **raw request body** refers to the exact byte sequence
received in the HTTP request body.

It is important because:
- cryptographic signatures are computed over raw bytes
- re-serializing JSON may change formatting
- signature verification may fail if the body is modified

Receivers should read and preserve the raw body
before any parsing or transformation.

---

## HTTP status code

An **HTTP status code** indicates the outcome
of an HTTP request.

In webhook systems:
- `2xx` signals successful receipt
- non-`2xx` may trigger retries by the provider

Webhook receivers should return stable and predictable status codes
to control provider retry behavior.

---

## 2xx response

HTTP status code indicating successful handling of a request.

Most webhook providers interpret any 2xx response
as confirmation that the event was accepted.

Returning 2xx does not necessarily mean
that all internal processing has completed.

---

## Timeout

A **timeout** occurs when the receiver
does not respond within the provider’s expected time window.

Timeouts often result in retries
and duplicate deliveries.

Webhook receivers should:
- respond quickly
- avoid long-running work in the request handler

---

## Event handler

Function or component responsible for processing a specific event type.

Handlers typically:
- contain business logic
- apply side effects
- validate event-specific data

Separating handlers by event type
improves clarity and maintainability.

---

## Dispatching

Process of routing an event to the appropriate handler based on its type.

This usually involves:
- inspecting the event type
- selecting the correct handler
- invoking it with the event data

Dispatching logic should be simple and explicit.

---

## Runbook

Operational document that describes how to diagnose and resolve issues.

Runbooks are used by:
- on-call engineers
- developers responding to incidents
- teams troubleshooting integrations

A good runbook focuses on symptoms, causes, and actions.

---

## ADR (Architecture Decision Record)

Short document that records an important architectural decision.

An ADR typically includes:
- context (the problem)
- decision (what was chosen)
- alternatives
- consequences

ADRs help future team members
understand why a system is designed the way it is.

---

## Observability

Refers to the ability to understand system behavior through signals such as:
- logs
- metrics
- traces

For webhook receivers, logs are especially important
for diagnosing delivery issues and retries.

---

## Logging

Practice of recording structured information about system behavior.

In webhook systems, logs often include:
- request identifiers
- event IDs
- event types
- processing outcomes

Good logging enables effective debugging and support.

---

## Replay attack

A replay attack occurs when an attacker captures a previously valid request
and resends it at a later time to trigger the same action again.

Signature verification alone does not prevent replay attacks, because a valid
signature remains valid if the request body is unchanged.

Mitigation strategies typically include timestamps, nonces, or idempotency checks.
Replay protection is documented as a future improvement for this template.


## Timestamp
A timestamp is a value included in a request that indicates when it was created.
When combined with signature verification, timestamps can be used to prevent
replay attacks by rejecting requests that are older than an allowed time window.

Timestamp-based validation is not implemented in this template but is referenced
as a possible future enhancement.
