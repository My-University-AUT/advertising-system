#!/bin/bash


# cd 
# source ./venv/bin/activate && celery -A aaic worker --loglevel=INFO --concurrency=8 -n worker1@%h

 
 NAME="Advertising Project - celery_worker_start"
 
PROJECT_DIR=/home/redhat/data/cloud-computing/advertising-system/advertisingSystem
ENV_DIR=/home/redhat/data/cloud-computing/advertising-system/advertisingSystem/venv/
 
 echo "Starting $NAME as `whoami`"
 
 # Activate the virtual environment
 cd "${PROJECT_DIR}"
 
 if [ -d "${ENV_DIR}" ]
 then
     . "${ENV_DIR}/bin/activate"
 fi

celery -A advertisingSystem worker --loglevel=INFO --concurrency=2 -n worker1@%h



# to stop running celery, use this command in django dir
# celery -A aaic control shutdown


# to kill flower
# pkill -9 -f 'flower'