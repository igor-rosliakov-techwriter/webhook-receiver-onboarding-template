# Local setup

This guide explains how to run the webhook receiver locally and send a sample request.

## Requirements
- Python 3.11+
- pip

## Project setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
make setup
```

## Environment configuration

The webhook receiver requires a shared secret to verify incoming webhook signatures.

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder value with your own secret:

```
WEBHOOK_SECRET=your_local_secret
```

> This secret is used only for local development.
> In real deployments, the secret is generated and managed by the webhook provider.

## Run the service locally

Start the webhook receiver:

```bash
make run
```

The service will start listening on `http://localhost:8000`.
> This command runs a long-lived server process and keeps the terminal busy.
> Leave this terminal open while testing the service.

## Send a signed webhook request

To test the service locally, you need to send a webhook request with a valid signature.

Open a **second terminal window** in the same repository and run:

```bash
make send
```

This command:
- Generates a valid HMAC signature using the shared secret from `.env`.
- Sends a sample webhook payload to the local service.
- Simulates a real webhook provider.

You should receive a `200 OK` response.
Sending the same request again will return:

```json
{
  "status": "duplicate"
}
```

## Troubleshooting

### Address already in use (Errno 48)

If you see an error like:

```
Address already in use
```

it means the service is already running in another terminal.
Stop the existing process or use a different port.

