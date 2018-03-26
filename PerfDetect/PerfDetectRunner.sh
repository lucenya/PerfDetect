#!/bin/bash

cd /home/PerfDetect
echo "Perf Detect task" >> /home/PerfDetect/log/auto_transfer.log 2>&1
python3 PerfDetect.py >> /home/PerfDetect/log/auto_transfer.log 2>&1