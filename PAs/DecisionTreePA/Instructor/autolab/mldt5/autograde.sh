#!/bin/bash
###
### Prologue.sh
###

# Setup
#if [[ -e data/ ]]; then
    # For people who want the data in the same location as the student's code
    #cp -r data/* working
    
    # For people who want the data in the directory the code is executed from
    #cp -r data/* .
    
    # Of course, the data is also in the data directory for those who want it there
#fi

#if [[ -e scaffolding ]]; then
#    cp -r scaffolding/* working
#fi

# Initialization that doesn't require the XML file

declare -A grades
grades=([WineTestTree]=0 [WineTestPredict]=0 [HiddenTestTree]=0 [HiddenTestPredict]=0)

status=0
success_of_previous_required=no

# General
declare -A max_score
max_score=([WineTestTree]=30 [WineTestPredict]=15 [HiddenTestTree]=15 [HiddenTestPredict]=15)

declare -A success_required
success_required=([Compile]="yes" [Style]="yes" [CompileOfficialTests]="yes" [OfficialTests]="no" )


###
### Tests
###

status=0
if [[  "$success_of_previous_required" = "no"  || $status -eq 0 ]]; then
   echo " "
   echo "Testing your code with the supplied wine test..."
   echo " "

   cp BinaryDT.py working

   DEPTH=2
   cp officialtests/* working
   cd working
   python3 RunDT.py wineTrainData.npy wineTrainLabel.npy ${DEPTH} > student.csv
   ##python3 RunDT.py wineTrainData.npy wineTrainLabel.npy ${DEPTH} 
   status=$?
   if [ $status -eq 0 ]
   then
     python3 TestDT.py winePrintOutput.csv student.csv
     status=$?
   else
     echo Student program did not execute properly 
     status=99
   fi
   
   if [ $status -eq 0 ] 
   then
       echo "  OK"
       grades[WineTestTree]=${max_score[WineTestTree]}
   else
       echo "  Your code does not pass the test of building the ."
       echo "  example wine data Decision Tree correctly."
       echo " "
   fi

   status=0
   if [ $status -eq 0 ] 
   then
       echo Testing predict function on example Wine Data
       python3 TestDTPredict.py wineTrainData.npy wineTrainLabel.npy \
               ${DEPTH} wineTestData.npy wineTestLabel.npy \
               wineTestLabelOfficialPredict.npy
       status=$?
       if [ $status -eq 0 ]
       then
	   echo Successful pass wine predictions
           grades[WineTestPredict]=${max_score[WineTestPredict]}
       else	
           echo Wine prediction set failed status code:${status}
       fi
   fi
fi


## Iris Dataset (hidden)
status=0
if [[  "$success_of_previous_required" = "no"  || $status -eq 0 ]]; then
   echo " "
   echo "Testing your code with the hidden case..."
   echo " "

   DEPTH=2
   python3 RunDT.py irisTrainData.npy irisTrainLabel.npy ${DEPTH} > student.csv
   status=$?
   if [ $status -eq 0 ]
   then
     python3 TestDT.py irisPrintOutput.csv student.csv
     status=$?
   else
     echo Student program did not execute properly 
     status=99
   fi
   
   if [ $status -eq 0 ] 
   then
       echo "  OK"
       grades[HiddenTestTree]=${max_score[HiddenTestTree]}
   else
       echo "  Your code does not pass the test of building the ."
       echo "  tree for the hidden dataset."
       echo " "
   fi

   status=0
   if [ $status -eq 0 ] 
   then
       echo Testing predict function on hidden dataset
       python3 TestDTPredict.py irisTrainData.npy irisTrainLabel.npy \
               ${DEPTH} irisTestData.npy irisTestLabel.npy \
               irisTestLabelOfficialPredict.npy
       status=$?
       if [ $status -eq 0 ]
       then
	   echo Successful pass hidden prediction test
           grades[HiddenTestPredict]=${max_score[HiddenTestPredict]}
       else 
           echo Failed hidden prediction test
       fi
   fi
fi

###
### Epilogue.sh
###

# Output the JSON map, but only for non-zero elements of the points array
first=1
printf "\n"
printf "{\"scores\": {"
for k in "${!max_score[@]}"; do
    if [[ ${max_score[$k]} -ne 0 ]]; then
	if [[ $first -eq 1 ]]; then
	    first=0
	    printf "\"%s\":%d" $k ${grades[$k]}
	else
	    printf ", \"%s\":%d" $k ${grades[$k]}
	fi
    fi
done
printf "}}\n" 

