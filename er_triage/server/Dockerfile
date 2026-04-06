# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# Use the official OpenEnv base image for a consistent runtime.
ARG BASE_IMAGE=ghcr.io/meta-pytorch/openenv-base:latest
FROM ${BASE_IMAGE} AS builder

WORKDIR /app

# Ensure git is available for VCS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Copy the entire environment source code into the image
# The build context should be the root of the 'er_triage' directory
COPY . /app/er_triage

WORKDIR /app/er_triage

# Ensure uv is available
RUN if ! command -v uv >/dev/null 2>&1; then \
        pip install uv; \
    fi

# Install dependencies using uv. This leverages caching for faster builds.
# It will use uv.lock if present, otherwise it resolves from pyproject.toml.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r requirements.txt

# Final, lean runtime stage
FROM ${BASE_IMAGE}

WORKDIR /app

# Copy the installed virtual environment from the builder stage
COPY --from=builder /app/er_triage/.venv /app/.venv

# Copy the application code
COPY --from=builder /app/er_triage /app/er_triage

# Add the virtual environment's bin to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Add the project root to PYTHONPATH to ensure modules are found
ENV PYTHONPATH="/app"

# Health check to ensure the server is running
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the FastAPI server using uvicorn
# The module path 'er_triage.server.app' corresponds to the file structure
CMD ["uvicorn", "er_triage.server.app:app", "--host", "0.0.0.0", "--port", "8000"]