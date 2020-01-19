#!/bin/bash

export PRESTO_DIR=/opt/presto

# Start Presto
/opt/presto/bin/launcher run

# Spin wait
while true; do sleep 1000; done