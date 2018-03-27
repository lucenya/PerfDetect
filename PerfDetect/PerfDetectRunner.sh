#!/bin/sh

rsyslogd
touch /var/log/cron.log
touch /var/log/perfdetect.log
start cron
echo "Perf Detect Start" >> /var/log/cron.log
tail -f /var/log/cron.log
