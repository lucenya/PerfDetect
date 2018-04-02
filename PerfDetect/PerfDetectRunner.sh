#!/bin/sh
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/open-xchange/sbin

touch /var/log/cron.log
#echo "00 08 * * * python3 /home/PerfDetect/PerfIcmAlert.py >> /var/log/cron.log 2>&1" >> mycron
echo "00 * * * * python3 /home/PerfDetect/PerfIcmAlert.py >> /var/log/cron.log 2>&1" >> mycron
crontab mycron
cron 
tail -f /var/log/cron.log
