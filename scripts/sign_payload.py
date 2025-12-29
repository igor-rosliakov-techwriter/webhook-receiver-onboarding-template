import argparse
import hashlib
import hmac
import os
from pathlib import Path

from dotenv import load_dotenv

def main():
    load_dotenv()

    p = argparse.ArgumentParser()
    p.add_argument("--secret", default=None, help="Override secret (otherwise WEBHOOK_SECRET from env/.env)")
    p.add_argument("--file", required=True, help="Payload file path")
    args = p.parse_args()

    secret = (args.secret or os.getenv("WEBHOOK_SECRET") or "").encode("utf-8")
    if not secret:
        raise SystemExit("WEBHOOK_SECRET is not set (use .env or --secret)")

    body = Path(args.file).read_bytes()
    sig = hmac.new(secret, body, hashlib.sha256).hexdigest()
    print(f"sha256={sig}")

if __name__ == "__main__":
    main()
