#!/bin/bash

WORK_DIR=$1
PYTHON_CMD=/usr/bin/python2.7
VERIFY=$WORK_DIR/verifydate.py
MY_PROC=$WORK_DIR/stockmain.py

cd $WORK_DIR
git pull
$PYTHON_CMD $VERIFY
if [ $? = 0 ]
then
	$PYTHON_CMD $MY_PROC
fi
