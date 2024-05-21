#!/bin/bash

# Ensure the environment variable is set
export LANG=C.UTF-8

# Start supervisord and have it manage the processes
supervisord -c ./supervisord.conf
