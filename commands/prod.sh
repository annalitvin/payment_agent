#!/bin/bash
gunicorn -w $NUM_WORKERS wsgi:app -b 0:$WSGI_PORT --log-level $LOG_LEVEL