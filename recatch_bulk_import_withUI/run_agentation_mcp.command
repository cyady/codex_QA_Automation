#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec npx -y agentation-mcp server
