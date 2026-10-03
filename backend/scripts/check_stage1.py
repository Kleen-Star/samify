"""Live Stage 1 check against the REAL MySQL database and running servers.

Run from backend/ with the venv active and the API running:
    python scripts/check_stage1.py
"""
import sys
import urllib.request
import json

from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import engine


def main() -> int:
    s = get_settings()
    ok = True
    print("Env loaded: APP_ENV =", s.app_env, "| SECRET_KEY set:", bool(s.secret_key))
    try:
        with engine.connect() as c:
            print("MySQL version:", c.execute(text("SELECT VERSION()")).scalar())
    except Exception as e:  # noqa: BLE001
        print("FAIL MySQL:", type(e).__name__)
        ok = False
    for url in ("http://localhost:8000/api/health", "http://localhost:5173/api/health"):
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                print("OK", url, json.loads(r.read())["data"])
        except Exception as e:  # noqa: BLE001
            print("FAIL", url, type(e).__name__)
            ok = False
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
