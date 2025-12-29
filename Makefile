.PHONY: help setup run sig send send-payload

# defaults (can be overridden: make send PAYLOAD=...)
PORT ?= 8000
PAYLOAD ?= examples/payloads/payment_succeeded.json

help:
	@echo "Available commands:"
	@echo "  make setup            - install dependencies"
	@echo "  make run              - run the webhook receiver locally"
	@echo "  make sig              - generate signature for default payload"
	@echo "  make send             - send signed webhook using default payload"
	@echo "  make send PAYLOAD=... - send signed webhook using a specific payload"

setup:
	pip install -r requirements.txt

run:
	uvicorn src.app:app --reload --port $(PORT)

sig:
	python scripts/sign_payload.py --file $(PAYLOAD)

send:
	$(eval SIG := $(shell python scripts/sign_payload.py --file $(PAYLOAD)))
	@echo "Sending payload: $(PAYLOAD)"
	@echo "Signature: $(SIG)"
	curl -i -X POST "http://localhost:$(PORT)/webhooks" \
	  -H "Content-Type: application/json" \
	  -H "X-Signature: $(SIG)" \
	  --data-binary @$(PAYLOAD)
