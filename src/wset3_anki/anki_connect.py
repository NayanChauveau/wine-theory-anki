from __future__ import annotations

import json
import os
import platform
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_ANKI_CONNECT_URL = "http://127.0.0.1:8765"
ANKI_CONNECT_ADDON_CODE = "2055492159"


class AnkiConnectError(RuntimeError):
    """Raised when AnkiConnect cannot complete a request."""


def _request(
    action: str,
    *,
    params: dict[str, object] | None = None,
    endpoint: str = DEFAULT_ANKI_CONNECT_URL,
    api_key: str | None = None,
    timeout: float = 30,
) -> Any:
    payload: dict[str, object] = {"action": action, "version": 6}
    if params is not None:
        payload["params"] = params
    if api_key:
        payload["key"] = api_key

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise AnkiConnectError(f"cannot reach AnkiConnect at {endpoint}: {exc}") from exc

    if not isinstance(result, dict) or "error" not in result:
        raise AnkiConnectError(f"unexpected AnkiConnect response for {action!r}")
    if result["error"] is not None:
        raise AnkiConnectError(f"AnkiConnect {action} failed: {result['error']}")
    return result.get("result")


def _launch_anki() -> None:
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["open", "-a", "Anki"], check=True)
        elif system == "Windows":
            subprocess.Popen(["cmd", "/c", "start", "", "Anki"])
        else:
            subprocess.Popen(["anki"])
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AnkiConnectError(f"could not start Anki Desktop: {exc}") from exc


def _wait_until_ready(
    *,
    endpoint: str,
    api_key: str | None,
    launch: bool,
    startup_timeout: float,
) -> None:
    try:
        _request("version", endpoint=endpoint, api_key=api_key, timeout=2)
        return
    except AnkiConnectError:
        if launch:
            _launch_anki()

    deadline = time.monotonic() + startup_timeout
    while time.monotonic() < deadline:
        try:
            _request("version", endpoint=endpoint, api_key=api_key, timeout=2)
            return
        except AnkiConnectError:
            time.sleep(0.5)

    raise AnkiConnectError(
        f"AnkiConnect did not become available at {endpoint}. "
        f"Install add-on {ANKI_CONNECT_ADDON_CODE}, restart Anki, and try again."
    )


def push_packages(
    packages: list[Path],
    *,
    endpoint: str | None = None,
    api_key: str | None = None,
    launch: bool = True,
    startup_timeout: float = 30,
) -> None:
    """Import packages into Anki Desktop, then synchronize once with AnkiWeb."""
    resolved = [package.resolve() for package in packages]
    missing = [str(package) for package in resolved if not package.is_file()]
    if missing:
        raise AnkiConnectError(f"missing package(s): {', '.join(missing)}")

    endpoint = endpoint or os.environ.get("ANKI_CONNECT_URL", DEFAULT_ANKI_CONNECT_URL)
    api_key = api_key or os.environ.get("ANKI_CONNECT_KEY")
    _wait_until_ready(
        endpoint=endpoint,
        api_key=api_key,
        launch=launch,
        startup_timeout=startup_timeout,
    )

    for package in resolved:
        _request(
            "importPackage",
            params={"path": str(package)},
            endpoint=endpoint,
            api_key=api_key,
        )
    _request("sync", endpoint=endpoint, api_key=api_key, timeout=120)
