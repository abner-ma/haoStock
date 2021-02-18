#!/bin/bash

WORK_DIR=`pwd`
PYTHON_CMD=python3
VERIFY=$WORK_DIR/common/verifydate.py
MY_PROC=$WORK_DIR/main/main.py

cd $WORK_DIR
$PYTHON_CMD $VERIFY
if [ $? = 0 ]
then
        $PYTHON_CMD $MY_PROC -o result.txt
fi
