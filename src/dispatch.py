from __future__ import annotations

from collections.abc import Callable
import logging

from .models import WebhookEvent
from .handlers import handle_payment_failed, handle_payment_succeeded

Handler = Callable[[WebhookEvent, logging.Logger], None]

HANDLERS: dict[str, Handler] = {
    "payment_succeeded": handle_payment_succeeded,
    "payment_failed": handle_payment_failed,
}


def dispatch(event: WebhookEvent, logger: logging.Logger) -> str:
    """
    Returns a result string for the HTTP response status field:
      - "ok"      -> handler executed
      - "ignored" -> unknown event type
    """
    handler = HANDLERS.get(event.type)
    if handler is None:
        logger.warning("unknown_event_type type=%s event_id=%s", event.type, event.id)
        return "ignored"

    handler(event, logger)
    return "ok"
