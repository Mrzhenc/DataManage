#!/bin/bash

#bak type file
cp /opt/DataManage/type / -rf

cd /opt/DataManage/
python /opt/DataManage/Start.py &
