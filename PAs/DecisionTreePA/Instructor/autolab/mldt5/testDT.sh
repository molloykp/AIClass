#!/bin/bash

# Machine Learning -- script to test/eval students decision tree class
# molloykp -- Sept 2019

#
# Tests
# Creates a directory named working, copies student code (BinaryDT.py)
# into this directory and verifies the tree constructed matches
# the basecase
#

OFFICIAL_TEST_DIR=officialtests

WINE_TRAIN_DATA=wineTrainData.npy
WINE_TRAIN_LABEL=wineTrainLabel.npy
WINE_TEST_DATA=wineTestData.npy
WINE_TEST_LABEL=wineTestLabel.npy
WINE_TREE_BASELINE=winePrintOutput.csv
WINE_PREDICT_BASELINE=wineTestLabelOfficialPredict.npy

RUN_DT=RunDT.py
TEST_DT_PREDICT=TestDTPredict.py
TEST_DT=TestDT.py

BINARY_DT=BinaryDT.py

# make sure that offcial test files are present
checkAFile()
{
  FILE_NAME=${1}
  localStatus=0
  if [ ! -r ${FILE_NAME} ]
  then
    echo Could not find file ${FILE_NAME}
    localStatus=1
  fi
  return ${localStatus}
}

checkFiles()
{
  status=0

  checkAFile ${OFFICIAL_TEST_DIR}/${WINE_TRAIN_DATA}
  let status=${status}+$?

  checkAFile ${OFFICIAL_TEST_DIR}/${WINE_TRAIN_LABEL}
  let status=${status}+$?

  checkAFile ${OFFICIAL_TEST_DIR}/${WINE_TEST_DATA}
  let status=${status}+$?

  checkAFile ${OFFICIAL_TEST_DIR}/${WINE_TEST_LABEL}
  let status=${status}+$?

  checkAFile ${OFFICIAL_TEST_DIR}/${WINE_TREE_BASELINE}
  let status=${status}+$?

  checkAFile ${OFFICIAL_TEST_DIR}/${WINE_PREDICT_BASELINE}
  let status=${status}+$?

  checkAFile ${OFFICIAL_TEST_DIR}/${RUN_DT}
  let status=${status}+$?

  checkAFile ${OFFICIAL_TEST_DIR}/${TEST_DT_PREDICT}
  let status=${status}+$?

  checkAFile ${OFFICIAL_TEST_DIR}/${TEST_DT}
  let status=${status}+$?

  checkAFile ${BINARY_DT}
  let status=${status}+$?

  return $status

}

checkFiles
status=$?
if [ $status -ne 0 ]
then
  echo Required files are not present, exiting...
  exit ${status}
fi

## Create a subdirectory to do all our work
if [ ! -d working ]
then
  mkdir working
else
  echo PLEASE NOTE THAT data in working will be copied over
fi

cp BinaryDT.py working
cp officialtests/* working
cd working

STUDENT_WINE_TREE_FILE=student.csv
python3 ${RUN_DT} ${WINE_TRAIN_DATA} ${WINE_TRAIN_LABEL} > ${STUDENT_WINE_TREE_FILE}
status=$?
if [ $status -eq 0 ]
then
  python3 ${TEST_DT} ${WINE_TREE_BASELINE} ${STUDENT_WINE_TREE_FILE}
  status=$?
else
  echo Student program did not execute properly 
  status=99
fi
   
if [ $status -eq 0 ] 
then
  echo "Tree verified successfully"
else
  echo "Your code does not output the expected decision tree "
  echo "for the example wine data."
  echo " "
fi

if [ $status -eq 0 ] 
then
  echo Testing predict function on example Wine Data
  DEPTH=2
  python3 ${TEST_DT_PREDICT} ${WINE_TRAIN_DATA} ${WINE_TRAIN_LABEL} ${DEPTH} \
            ${WINE_TEST_DATA} ${WINE_TEST_LABEL} \
            ${WINE_PREDICT_BASELINE}
  status=$?
  if [ $status -eq 0 ]
  then
    grades[WineTestPredict]=${max_score[WineTestPredict]}
  fi
fi
