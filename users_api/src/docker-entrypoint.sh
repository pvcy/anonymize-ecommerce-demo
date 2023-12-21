#!/bin/bash

gunicorn --workers 2 \
-b 0.0.0.0:8000 \
users_api:app \
--access-logfile -
