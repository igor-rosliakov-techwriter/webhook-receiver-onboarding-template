from __future__ import annotations

import logging

def handle_payment_succeeded(payload: dict, logger: logging.Logger, request_id: str) -> None:
    event_id = payload.get("id") or payload.get("event_id")
    logger.info(
        "handler_payment_succeeded",
        extra={"request_id": request_id, "event_id": event_id},
    )

def handle_payment_failed(payload: dict, logger: logging.Logger, request_id: str) -> None:
    event_id = payload.get("id") or payload.get("event_id")
    reason = (payload.get("data") or {}).get("reason")
    logger.info(
        "handler_payment_failed",
        extra={"request_id": request_id, "event_id": event_id, "reason": reason},
    )
