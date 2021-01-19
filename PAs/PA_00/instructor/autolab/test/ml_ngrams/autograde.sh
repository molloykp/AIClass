#!/bin/bash
###
### Prologue.sh
###

echo arg count is $#
if [ $# -eq 1 ]
then
  echo print arg 1 is: ${1}
fi

#if [[ -e scaffolding ]]; then
#    cp -r scaffolding/* working
#fi

# Initialization that doesn't require the XML file

declare -A grades
grades=([bigrams]=0 [trigrams]=0)

status=0
success_of_previous_required=no

# General
declare -A max_score
max_score=([bigrams]=50 [trigrams]=15)

declare -A success_required
success_required=([Compile]="yes" [Style]="yes" [CompileOfficialTests]="yes" [OfficialTests]="no" )


###
### Tests
###

status=0
SRCFILE=text_gen.py

if [[  "$success_of_previous_required" = "no"  || $status -eq 0 ]]
then
   echo " "
   echo "Testing your code..."
   echo " "

   if [ ! -f ${SRCFILE} ]
   then
     echo Source file ${SRCFILE} not found
     exit -1
   else
     cp ${SRCFILE} working
   fi
   cp officialtests/text_gen_tests.py working
   cp officialtests/unittest_utils.py working
   cd working
   python3 text_gen_tests.py 
   points=$?
   #echo points are $points
   if [ $status -eq 0 ] 
   then
       grades[bigrams]=${points}
       grades[trigrams]=15
   else
       echo "  Your code does not pass the test of building the ."
       echo "  example wine data Decision Tree correctly."
       echo " "
   fi
fi
