"""Load local secrets without ever printing them."""
from __future__ import annotations

import os
from pathlib import Path


def load(project_root: Path | None = None) -> None:
    """Populate unset environment variables from a local .env file.

    Uses python-dotenv when installed; the small fallback keeps the project usable
    before dependencies are installed. Existing environment variables always win.
    """
    root = project_root or Path(__file__).resolve().parents[1]
    env_file = root / ".env"
    if not env_file.exists():
        return
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file, override=False)
        return
    except ImportError:
        pass
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
