#!/usr/bin/env python3
"""Run the frontend static server and FastAPI backend together."""

from __future__ import annotations

import argparse
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".env"
FRONTEND_DIR = REPO_ROOT / "frontend"
BACKEND_DIR = REPO_ROOT / "backend"


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


def env_value(name: str, file_values: dict[str, str], default: str) -> str:
    return os.environ.get(name, file_values.get(name, default))


def positive_port(value: str) -> int:
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return port


def build_parser(file_values: dict[str, str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Start the MuslimConnect frontend and backend together.",
    )
    parser.add_argument(
        "--frontend-host",
        default=env_value("FRONTEND_HOST", file_values, "127.0.0.1"),
        help="Host interface for the frontend static server.",
    )
    parser.add_argument(
        "--frontend-port",
        type=positive_port,
        default=positive_port(env_value("FRONTEND_PORT", file_values, "5500")),
        help="Port for the frontend static server.",
    )
    parser.add_argument(
        "--backend-host",
        default=env_value(
            "BACKEND_HOST",
            file_values,
            env_value("APP_HOST", file_values, "127.0.0.1"),
        ),
        help="Host interface for the FastAPI backend.",
    )
    parser.add_argument(
        "--backend-port",
        type=positive_port,
        default=positive_port(
            env_value(
                "BACKEND_PORT",
                file_values,
                env_value("APP_PORT", file_values, "8000"),
            ),
        ),
        help="Port for the FastAPI backend.",
    )
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable Uvicorn auto-reload.",
    )
    return parser


def pick_python() -> Path:
    venv_python = REPO_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return venv_python
    return Path(sys.executable)


def ensure_path_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"{label} not found: {path}")


def ensure_port_available(name: str, host: str, port: int) -> None:
    bind_error: OSError | None = None
    addrinfo = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)

    for family, socktype, proto, _, sockaddr in addrinfo:
        sock = socket.socket(family, socktype, proto)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(sockaddr)
            return
        except OSError as exc:
            bind_error = exc
        finally:
            sock.close()

    detail = f"{host}:{port}"
    raise SystemExit(
        f"{name} port {detail} is unavailable ({bind_error}). "
        f"Choose another port with --{name.lower()}-port."
    )


def display_host(host: str) -> str:
    if host in {"0.0.0.0", "::"}:
        return "127.0.0.1"
    return host


def wait_for_url(url: str, process: subprocess.Popen[bytes], timeout: float = 15.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process.poll() is not None:
            return False
        try:
            with urlopen(url, timeout=1) as response:
                return 200 <= response.status < 500
        except URLError:
            time.sleep(0.25)
    return False


def stop_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> int:
    file_values = load_env_file(ENV_FILE)
    parser = build_parser(file_values)
    args = parser.parse_args()

    if args.frontend_port == args.backend_port:
        raise SystemExit("Frontend and backend must use different ports.")

    ensure_path_exists(FRONTEND_DIR, "Frontend directory")
    ensure_path_exists(BACKEND_DIR, "Backend directory")

    ensure_port_available("frontend", args.frontend_host, args.frontend_port)
    ensure_port_available("backend", args.backend_host, args.backend_port)

    python_executable = pick_python()
    reload_enabled = not args.no_reload

    frontend_cmd = [
        str(python_executable),
        "-m",
        "http.server",
        str(args.frontend_port),
        "--bind",
        args.frontend_host,
        "--directory",
        str(FRONTEND_DIR),
    ]
    backend_cmd = [
        str(python_executable),
        "-m",
        "uvicorn",
        "app.main:app",
        "--app-dir",
        str(BACKEND_DIR),
        "--host",
        args.backend_host,
        "--port",
        str(args.backend_port),
    ]
    if reload_enabled:
        backend_cmd.append("--reload")

    print("Starting MuslimConnect dev services...")
    print(f"Frontend command: {' '.join(frontend_cmd)}")
    print(f"Backend command: {' '.join(backend_cmd)}")
    print("Press Ctrl+C to stop both servers.\n")

    frontend_process = subprocess.Popen(frontend_cmd, cwd=REPO_ROOT)
    backend_process = subprocess.Popen(backend_cmd, cwd=REPO_ROOT)

    local_frontend_host = display_host(args.frontend_host)
    local_backend_host = display_host(args.backend_host)
    frontend_url = f"http://{local_frontend_host}:{args.frontend_port}/web-landing.html"
    dashboard_url = f"http://{local_frontend_host}:{args.frontend_port}/web-dashboard.html"
    backend_health_url = f"http://{local_backend_host}:{args.backend_port}/api/v1/health"
    backend_events_url = f"http://{local_backend_host}:{args.backend_port}/api/v1/events/upcoming"
    backend_docs_url = f"http://{local_backend_host}:{args.backend_port}/docs"

    try:
        frontend_ready = wait_for_url(
            f"http://{local_frontend_host}:{args.frontend_port}/web-landing.html",
            frontend_process,
        )
        backend_ready = wait_for_url(backend_health_url, backend_process)

        if not frontend_ready or not backend_ready:
            raise RuntimeError("One or more dev services exited before becoming ready.")

        print("Dev services are ready:")
        print(f"  Frontend landing page: {frontend_url}")
        print(f"  Frontend dashboard:    {dashboard_url}")
        print(f"  Backend health:        {backend_health_url}")
        print(f"  Backend events:        {backend_events_url}")
        print(f"  Backend docs:          {backend_docs_url}\n")

        while True:
            frontend_code = frontend_process.poll()
            backend_code = backend_process.poll()

            if frontend_code is not None:
                print(f"Frontend server exited with code {frontend_code}.")
                return frontend_code
            if backend_code is not None:
                print(f"Backend server exited with code {backend_code}.")
                return backend_code

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping dev services...")
        return 0
    finally:
        stop_process(frontend_process)
        stop_process(backend_process)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_args: sys.exit(0))
    raise SystemExit(main())
