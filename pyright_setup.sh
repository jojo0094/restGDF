#!/bin/bash

# Script to create pyrightconfig.json pointing to a local .venv folder

PROJECT_ROOT="$(pwd)"
VENV_DIR=".venv"

# Check if .venv exists
if [ ! -d "$PROJECT_ROOT/$VENV_DIR" ]; then
  echo "❌ Error: '$VENV_DIR' folder not found in project root: $PROJECT_ROOT"
  exit 1
fi

# Write pyrightconfig.json
cat > pyrightconfig.json <<EOF
{
  "venvPath": "$PROJECT_ROOT",
  "venv": "$VENV_DIR"
}
EOF

echo "✅ pyrightconfig.json created:"
cat pyrightconfig.json
