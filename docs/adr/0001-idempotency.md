# ADR-0001: Idempotency for webhook processing

## Status
Draft

## Context

Webhook providers may retry event deliveries in cases of network failures,
timeouts, or non-2xx HTTP responses.
As a result, the same event can be delivered multiple times.

Without special handling, this may lead to duplicate processing
and unintended side effects.

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
