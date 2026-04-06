# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the ER Triage Environment.

This module creates an HTTP server that exposes the ERTriageEnvironment
over HTTP and WebSocket endpoints, compatible with EnvClient.
"""

try:
    from openenv.core.env_server.http_server import create_app
except ImportError as e:
    raise ImportError(
        "openenv-core is required for the web interface. "
        "Install dependencies with 'pip install \"openenv-core[core]\"' or 'uv pip install \"openenv-core[core]\"'"
    ) from e

# Use a try-except block for robust imports
try:
    from ..models import ERTriageAction, ERTriageObservation
    from .environment import ERTriageEnvironment
except (ImportError, ModuleNotFoundError):
    # This path is for direct execution or when the package is not installed
    from models import ERTriageAction, ERTriageObservation
    from server.environment import ERTriageEnvironment


# Create the FastAPI app using the core http_server factory
app = create_app(
    ERTriageEnvironment,
    ERTriageAction,
    ERTriageObservation,
    env_name="er_triage",
    max_concurrent_envs=10,  # Allow multiple concurrent WebSocket sessions
)


def main(host: str = "0.0.0.0", port: int = 8000):
    """
    Entry point for direct execution.
    Example: python -m er_triage.server.app
    """
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the ER Triage FastAPI server.")
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind the server to."
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to run the server on."
    )
    args = parser.parse_args()
    main(host=args.host, port=args.port)