#!/bin/bash

#echo arg count is $#
#if [ $# -eq 1 ]
#then
#  echo print arg 1 is: ${1}
#fi

###
### Tests
###

status=0
SRCFILE=decision_tree.py

echo " "
echo "Testing your code..."
echo " "

if [ ! -f ${SRCFILE} ]
then
  echo Source file ${SRCFILE} not found
  exit -1
fi

cp ${SRCFILE} working

cp officialtests/decision_tree_tests.py working
cp officialtests/decision_tree_tests_hidden.py working
cp officialtests/unittest_utils.py working

cd working

python3 decision_tree_tests_hidden.py 
exit 0
