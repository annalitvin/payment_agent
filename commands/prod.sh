#!/bin/bash
-c 'while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g \"daemon off;\"'
gunicorn -w $NUM_WORKERS wsgi:app -b 0:$WSGI_PORT --log-level $LOG_LEVEL
