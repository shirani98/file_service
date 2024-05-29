#!/bin/bash

CLIENT_IP=$1
REMOTE_DIR=$2
LOCAL_DIR="/home/mahdi/test_server"  # Change_data

rsync -avz -e ssh "$LOCAL_DIR" "user@$REMOTE_IP:$REMOTE_DIR"