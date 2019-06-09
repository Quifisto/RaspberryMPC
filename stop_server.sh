#!/bin/sh

# Check if the server is actually running
server_pid=$(pgrep -f server.py)
[ "$server_pid" != "" ] && kill $server_pid
