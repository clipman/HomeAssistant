#!/usr/bin/env bash
set -e

export WEBHOOK_URL="$(jq -r '.webhook_url' /data/options.json)"

python /app/server.py
