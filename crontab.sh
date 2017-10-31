#!/bin/bash

(crontab -l 2>/dev/null; echo "00 * * * * python /var/www/backupy/run.py") | crontab -
