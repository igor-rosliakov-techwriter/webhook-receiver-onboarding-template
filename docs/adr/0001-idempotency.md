# ADR-0001: Idempotency for webhook processing

## Context

Webhook providers deliver events over HTTP and do not have reliable knowledge
of whether an event was successfully processed by the receiving system.

If the receiver:
- does not respond,
- responds with a non-2xx status code,
- or responds too slowly,

the provider may retry the delivery of the same event. As a result, the same 
logical event can be delivered multiple times.

In systems that perform side effects (such as creating orders or charging payments),
processing the same event more than once may lead to incorrect behavior.

For example, if a `payment_succeeded` event is delivered twice and the system is not idempotent:
- the payment may be recorded multiple times,
- the same order may be created more than once.

To ensure correct behavior, duplicate deliveries must be expected and handled explicitly.

## Decision

The service will treat webhook processing as idempotent. Each incoming event is 
identified by a unique event identifier (`event_id`) provided in the webhook payload.
The service keeps track of processed event identifiers and ignores duplicate 
deliveries of the same event.

In the current implementation, processed event identifiers are stored
in an in-memory set. This approach is intentionally simple and suitable for local 
development, onboarding examples, and documentation purposes.


## Alternatives considered

- No deduplication  
  Rejected due to the high risk of duplicate side effects when webhook
  providers retry event delivery.
- Deduplication using an in-memory store  
  Accepted for the current implementation.  
  Suitable for local development and demonstration purposes, but does not
  persist state across restarts.
- Deduplication using an external store (e.g. Redis or database)  
  Considered the preferred approach for a production system, as it allows
  idempotency guarantees across restarts and multiple instances.

## Consequences

- Duplicate deliveries of the same event are safely ignored.
- The service returns a successful response (`200 OK`) for duplicate events
  to prevent repeated retries by the webhook provider.
- Idempotency state is lost when the service restarts, as the current
  implementation uses in-memory storage.

This trade-off is acceptable for local development and onboarding purposes.
A persistent store would be required for production use.

## Configuration note

The choice of idempotency storage is reflected in the environment configuration:

```env
IDEMPOTENCY_STORE=in-memory
```

This value documents the currently implemented approach.
Alternative backends (e.g. Redis or database) are intentionally left
as planned extensions.
