from __future__ import annotations

from collections.abc import Callable
import logging

from .handlers import (
    andle_payment_failed,
    handle_payment_succeeded,
    handle_subscription_created,
)


Handler = Callable[[dict, logging.Logger, str], None]

HANDLERS: dict[str, Handler] = {
    "payment_succeeded": handle_payment_succeeded,
    "payment_failed": handle_payment_failed,
    "subscription_created": handle_subscription_created,
}

def dispatch_event(event_type: str, payload: dict, logger: logging.Logger, request_id: str) -> str:
    """
    Executes a handler for known event types.

    Returns:
      - "ok"      if handler executed
      - "ignored" if event type is unknown
    """
    handler = HANDLERS.get(event_type)
    if handler is None:
        logger.warning(
            "webhook_ignored_unknown_event_type",
            extra={"request_id": request_id, "event_type": event_type},
        )
        return "ignored"

    handler(payload, logger, request_id)
    return "ok"
