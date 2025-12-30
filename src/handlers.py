from __future__ import annotations

from typing import Any
import logging

from .models import WebhookEvent


def handle_payment_succeeded(event: WebhookEvent, logger: logging.Logger) -> None:
    # minimal "business logic" – just show where real work would happen
    logger.info("handler:payment_succeeded event_id=%s", event.id)


def handle_payment_failed(event: WebhookEvent, logger: logging.Logger) -> None:
    logger.info("handler:payment_failed event_id=%s", event.id)
