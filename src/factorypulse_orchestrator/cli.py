from __future__ import annotations

import argparse
import json

import uvicorn

from factorypulse_api.app import create_app
from factorypulse_api.settings import Settings

from .runner import run


def main() -> None:
    parser = argparse.ArgumentParser(prog="factorypulse-run")
    commands = parser.add_subparsers(dest="command", required=True)
    execute = commands.add_parser("run", help="produce a full FactoryPulse artifact set")
    execute.add_argument("--workspace", default="artifacts/factorypulse-run")
    execute.add_argument("--count", type=int, default=120)
    execute.add_argument("--fault-after", type=int, default=85)
    serve = commands.add_parser("serve", help="serve a prepared API data directory")
    serve.add_argument("--workspace", default="artifacts/factorypulse-run")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.command == "run":
        print(json.dumps(run(args.workspace, args.count, args.fault_after), indent=2))
    else:
        uvicorn.run(create_app(Settings.from_directory(f"{args.workspace}/api-data")), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
