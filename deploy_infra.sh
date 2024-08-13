#!/bin/bash
cd /home/terraform
tflocal init
tflocal apply -auto-approve
cd /home/functions
python create_table.py

cd /home/IoTSensors
pip install --no-cache-dir -r requirements.txt
python factory.py 50 5