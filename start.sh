#!/bin/bash
mkdir -p /tmp/.cache
export XDG_CACHE_HOME=/tmp/.cache
gunicorn -w 4 -b 0.0.0.0:5000 aiReadinessbackend:app

