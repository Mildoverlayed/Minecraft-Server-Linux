#!/bin/bash

SESSION="minecraft-server"

# Start a new tmux session, split vertically (left/right)
tmux new-session -d -s $SESSION

# Run the Python script in the left pane (pane 0)
tmux send-keys -t $SESSION 'python3 server.py' C-m

# Split the window vertically (right pane)
tmux split-window -h -t $SESSION

# Run gotop in the right pane (pane 1)
tmux send-keys -t $SESSION:0.1 'gotop' C-m

# Attach to the session
tmux attach -t $SESSION