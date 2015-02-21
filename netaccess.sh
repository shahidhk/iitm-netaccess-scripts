#!/bin/bash
#title           : netaccess.sh
#description     : This script will authenticate the device with IIT Madras Netaccess.
#usage           : sh netaccess.sh <username> <password>
#author          : Shahidh K Muhammed - muhammedshahid.k@gmail.com
#init-date       : 22-02-2015
#version         : 0.1
#=======================================================================================

DTIME=`date +%Y%m%d%M%S`
CURL_TMP1="/tmp/netaccess-bash-script-${DTIME}.tmp"
CURL_TMP2="/tmp/netaccess-bash-script-${DTIME}.tmp"

if [ $# -lt 2 ]
  then
    echo "Not enough arguments! Usage: ./netaccess.sh <username> <password>"
    exit
fi

USERNAME=$1
PASSWORD=$2


curl -s -d "userLogin=${USERNAME}&userPassword=${PASSWORD}" --dump-header headers https://netaccess.iitm.ac.in/account/login > ${CURL_TMP1}
curl -L -s -b headers -X POST https://netaccess.iitm.ac.in/account/approve -d "duration=2&approveBtn=" > ${CURL_TMP2}

CURL_TST=`cat ${CURL_TMP2} | grep -c "<span class='label label-success'>Active</span>"`

if [ ${CURL_TST} -eq 1 ]
then
        STATUS_CODE=0
        STATUS="Authenticated!"
else
        STATUS_CODE=1
        STATUS="Error! Invalid username/password or Network not reachable!"
fi

if [ -f ${CURL_TMP1} ]; then
        rm -f ${CURL_TMP1}
        rm -f ${CURL_TMP2}
fi
echo ${STATUS}

exit ${STATUS_CODE}
