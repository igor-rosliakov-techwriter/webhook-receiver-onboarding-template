from pydantic import BaseModel
from typing import Any


class WebhookEvent(BaseModel):
    id: str
    type: str
    data: dict[str, Any] = {}
