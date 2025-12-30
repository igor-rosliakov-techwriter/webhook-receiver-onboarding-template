import hashlib
import hmac
import json
import logging
import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .dispatch import dispatch_event

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("webhook_receiver")

app = FastAPI(title="Webhook Receiver (Onboarding Template)")

SIGNATURE_HEADER = "X-Signature"
SIGNATURE_PREFIX = "sha256="

processed_event_ids: set[str] = set()


def compute_signature(secret: str, raw_body: bytes) -> str:
    """
    Compute HMAC-SHA256 over raw request body bytes and return value formatted
    as: sha256=<hex_digest>
    """
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return f"{SIGNATURE_PREFIX}{digest}"


def verify_signature(secret: str, raw_body: bytes, received_signature: str | None) -> bool:
    """
    Verify request signature using constant-time comparison.
    """
    if not received_signature:
        return False
    expected = compute_signature(secret, raw_body)
    return hmac.compare_digest(expected, received_signature)


@app.post("/webhooks")
async def receive_webhook(request: Request):
    request_id = str(uuid.uuid4())

    raw_body = await request.body()

    secret = os.getenv("WEBHOOK_SECRET")
    if not secret:
        logger.error(
            "webhook_misconfigured",
            extra={"request_id": request_id, "status": "missing_webhook_secret"},
        )
        return JSONResponse(
            status_code=500,
            content={
                "request_id": request_id,
                "error": "server_misconfigured",
                "message": "WEBHOOK_SECRET is not configured.",
            },
        )

    received_signature = request.headers.get(SIGNATURE_HEADER)
    if not verify_signature(secret, raw_body, received_signature):
        logger.info(
            "webhook_rejected",
            extra={
                "request_id": request_id,
                "status": "invalid_signature",
            },
        )
        return JSONResponse(
            status_code=401,
            content={
                "request_id": request_id,
                "error": "invalid_signature",
                "message": "Request signature is missing or invalid.",
            },
        )

    body_text = raw_body.decode("utf-8", errors="replace")

    try:
        payload = json.loads(body_text) if body_text else {}
    except json.JSONDecodeError:
        logger.info(
            "webhook_received",
            extra={
                "request_id": request_id,
                "status": "invalid_json",
            },
        )
        return JSONResponse(
            status_code=400,
            content={
                "request_id": request_id,
                "error": "invalid_json",
                "message": "Request body must be valid JSON.",
            },
        )

    # idempotency key
    event_id = payload.get("id") or payload.get("event_id")
    if not event_id:
        logger.info(
            "webhook_received",
            extra={
                "request_id": request_id,
                "status": "missing_event_id",
            },
        )
        return JSONResponse(
            status_code=400,
            content={
                "request_id": request_id,
                "error": "missing_event_id",
                "message": "Payload must include an event id (id/event_id).",
            },
        )

    event_type = payload.get("type") or payload.get("event_type") or "unknown"

    # deduplicate deliveries
    if event_id in processed_event_ids:
        logger.info(
            "webhook_duplicate_ignored",
            extra={
                "request_id": request_id,
                "event_id": event_id,
                "event_type": event_type,
                "status": "duplicate",
            },
        )
        return {
            "request_id": request_id,
            "status": "duplicate",
            "event_id": event_id,
            "event_type": event_type,
        }

    processed_event_ids.add(event_id)

    processed_event_ids.add(event_id)

    result = dispatch_event(event_type=event_type, payload=payload, logger=logger, request_id=request_id)
    
    logger.info(
        "webhook_received",
        extra={
            "request_id": request_id,
            "event_id": event_id,
            "event_type": event_type,
            "status": result,  # <-- было "ok"
        },
    )
    
    return {
        "request_id": request_id,
        "status": result,  # <-- было "ok"
        "event_id": event_id,
        "event_type": event_type,
    }

