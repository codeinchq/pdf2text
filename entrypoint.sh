#!/bin/sh

# Forward SIGTERM and SIGINT to the child process
trap "kill -TERM $CHILD_PID" TERM INT

# Run the actual application
uvicorn app:app --host 0.0.0.0 --port $PORT &

CHILD_PID=$!
wait $CHILD_PID