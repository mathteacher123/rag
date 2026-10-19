#!/bin/bash

# Check if an argument was provided
if [ -z "$1" ]; then
    echo "Usage: $0 {u|d}"
    echo "  u : Up (start docker)"
    echo "  d : Down (stop docker)"
    exit 1
fi

# Handle the argument
case "$1" in
    u)
        echo "Starting Docker containers..."
        docker compose --project-directory ~/freellmapi up -d
        ;;
    d)
        echo "Stopping Docker containers..."
        docker compose --project-directory ~/freellmapi down
        ;;
    *)
        echo "Invalid option: $1"
        echo "Use 'u' to start or 'd' to stop."
        exit 1
        ;;
esac
