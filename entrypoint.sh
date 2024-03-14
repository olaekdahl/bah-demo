#!/bin/bash
# entrypoint.sh

# Source the bashrc
source ~/.bashrc

# Execute the Docker CMD
exec "$@"
