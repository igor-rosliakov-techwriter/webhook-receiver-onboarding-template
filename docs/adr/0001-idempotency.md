# ADR-0001: Idempotency for webhook processing

## Status
Draft

## Context

Webhook providers deliver events over HTTP and do not have reliable knowledge
of whether an event was successfully processed by the receiving system.

If the receiver:
- does not respond,
- responds with a non-2xx status code,
- or responds too slowly,

the provider may retry the delivery of the same event.

As a result, the same logical event can be delivered multiple times.

In systems that perform side effects (such as creating orders or charging payments),
processing the same event more than once may lead to incorrect behavior.

For example, if a `payment_succeeded` event is delivered twice and the system is not idempotent:
- the payment may be recorded multiple times,
- the same order may be created more than once.

To ensure correct behavior, duplicate deliveries must be expected and handled explicitly.

## Decision

The service will treat webhook processing as idempotent.

Each incoming event will be identified by a unique event identifier,
and duplicate deliveries of the same event will not be processed more than once.

## Alternatives considered

- No deduplication  
  Rejected due to the high risk of duplicate side effects.

- Deduplication using an in-memory store  
  Suitable for local development and demonstration purposes.

- Deduplication using an external store (e.g. Redis or database)  
  Preferred approach for a production system.

## Consequences

- The service must rely on stable event identifiers.
- Additional storage is required to track processed events.
- A retention or expiration strategy is needed for stored identifiers.

(This ADR documents the intended design and will be revisited
as the implementation evolves.)
