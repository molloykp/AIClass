#!/bin/bash

#    name: makeWebSite.sh
# purpose: put files in place from repo to website
#          You need to run build.py to construct pdfs (from latex)
#          and possibly other objects.

copy_web_stuff()
{
  SDIR=${1}
  TDIR=${2}
  MOVEDIR=${3}
  SDIRSUB=${SDIR}/${MOVEDIR}
  TDIRSUB=${TDIR}/${MOVEDIR}

  if [ ! -d ${TDIRSUB} ] 
  then
    mkdir ${TDIRSUB}
  fi

  ls -1 ${SDIRSUB} | while read SUBDIR;
  do
    FROMDIR=${SDIRSUB}/${SUBDIR}/www
    TODIR=${TDIRSUB}/${SUBDIR}
    echo copying ${FROMDIR} to ${TODIR}
    if [ -d ${FROMDIR} ]
    then
      if [ ! -d ${TODIR} ]
      then
        mkdir ${TODIR}
      fi
      cp -R ${FROMDIR}/* ${TODIR}
  fi
done
}

## Copying programming assignments to the website

copy_PAs()
{
  SDIR=${1}
  TDIR=${2}
}



##
## MAIN
##

# arguments: directory where to deploy the class
if [ $# -ne 1 ]
then
  echo "makeWebSite.sh targetDirectory"
  exit 99
fi

SDIR=..
TDIR=${1}

# make sure directory exists
if [ ! -d ${TDIR} ]
then
  echo specified target directory ${TDIR} must exist
  echo prior to running this script
  exit 99
fi

cp -R /Users/kmolloy/teaching/cs445/MLWeb/molloykp ${TDIR}
cp -R ${SDIR}/wwwMolloy/*  ${TDIR}
cp -R ${SDIR}/weekGuides ${TDIR}
cp -R ${SDIR}/resources ${TDIR}

mkdir ${TDIR}/slides
cp ${SDIR}/slides/*.pdf ${TDIR}/slides

## for each PA, copy the student/website info (not the instructor info)
copy_web_stuff $SDIR $TDIR PAs
copy_web_stuff $SDIR $TDIR hw
copy_web_stuff $SDIR $TDIR mquizzes

cp $SDIR/wwwMolloy/PAs/PA.php $TDIR/PAs

## now labs
copy_web_stuff $SDIR $TDIR labs

THISHOST=`hostname`
echo $THISHOST
if [ "${THISHOST}" = "Kevins-MacBook-Pro.local" ]
then
  cp -R ~/teaching/molloykpwebFoot ${TDIR}/molloykp
fi

## copy the syllabus
cp ../cs444_Spring2021/cs444_Syllabus/cs444_2021Spring_Syllabus.pdf ${TDIR}
