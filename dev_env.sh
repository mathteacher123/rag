#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# 1. Terminal Shortcuts & Aliases
# -----------------------------------------------------------------------------
# Shortcut to start the Uvicorn web server
alias devserver='uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload'

# Function to test the POST chunking endpoint with a dynamic URL parameter
chunkurl() {
    if [ -z "$1" ]; then
        echo "❌ Error: Missing URL argument."
        echo "Usage: chunkurl <https://example.com>"
        return 1
    fi

    curl -X POST "https://github.dev" \
         -H "Content-Type: application/json" \
         -d "{\"url\": \"$1\"}"
}

# Print success messages for the shortcuts
echo "🚀 Workspace environment loaded successfully!"
echo "👉 Use 'devserver' to start the Uvicorn API server."
echo "👉 Use 'chunkurl <url>' to test the HTML chunking endpoint."

# -----------------------------------------------------------------------------
# 2. Automated Git & Cloud Environment Hooks
# -----------------------------------------------------------------------------
# Automate port forwarding optimization explicitly inside GitHub Codespaces
if [ -n "$CODESPACE_NAME" ]; then
    echo "⚡ GitHub Codespace detected ($CODESPACE_NAME)"
    
    # Ensure the GitHub CLI tool is installed before attempting execution
    if command -v gh &> /dev/null; then
        echo "🔄 Automatically updating visibility of port 8000 to public..."
        gh codespace ports visibility 8000:public -c "$CODESPACE_NAME"
        echo "✅ Port 8000 is now public."
    else
        echo "⚠️ Warning: 'gh' CLI tool is missing. Cannot modify port visibility."
    fi
fi
