#!/bin/sh

# If server is already running stop previous instance.
server_pid="$(pgrep -f server.py)"
[ "$server" != "" ] && kill "$server_pid"

# Wait for the previous instance to stop.
while [ "$server" != "" ]; do
    server_pid=$(pgrep -f "server.py")
done

# Start server and detach it, also redirect stdin and stdout to a log file
python3 ./server.py >log.txt 2>&1 &

