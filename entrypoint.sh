#!/bin/bash
python3 manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python3 manage.py migrate
fi
exec "$@"
