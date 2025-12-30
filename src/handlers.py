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

def handle_subscription_created(payload: dict, logger, request_id: str) -> None:
    event_id = payload.get("id") or payload.get("event_id")
    data = payload.get("data") or {}

    subscription_id = data.get("subscription_id")
    user_id = data.get("user_id")
    plan = data.get("plan")

    logger.info(
        "handler_subscription_created request_id=%s event_id=%s subscription_id=%s user_id=%s plan=%s",
        request_id,
        event_id,
        subscription_id,
        user_id,
        plan,
    )
