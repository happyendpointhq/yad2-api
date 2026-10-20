"""Minimal client for the Yad2 API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os
from datetime import datetime

import requests

HOST = "yad21.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` part of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def rows(data):
    """Reference endpoints wrap their list as {"paginator": ..., "data": [...]}."""
    return data["data"] if isinstance(data, dict) and "data" in data else data


def sale_date(deal):
    """Registered deals give saleDay as DD.MM.YY, for example "04.06.26" is 4 June 2026."""
    return datetime.strptime(deal["saleDay"], "%d.%m.%y").date()


def per_sqm(price, sqm):
    return round(price / sqm) if price and sqm else None
