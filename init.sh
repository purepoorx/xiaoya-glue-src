#!/bin/bash

DOCKER_ADDRESS=$(grep -i docker_address /strm.txt|tr -d '\r'|cut -f2 -d= |sed 's/\//\\\//g; s/\s\+$//g')
SCAN_PATHS=$(grep -n scan_path /strm.txt | cut -f1 -d:)
USERNAME=$(grep username /strm.txt|tr -d '\r'|cut -f2 -d= |sed 's/\s\+$//g')
PASSWORD=$(grep password /strm.txt|tr -d '\r'|cut -f2 -d= |sed 's/\s\+$//g')

for i in $SCAN_PATHS; do
	cp /strm.py /tmp/strm.py
	SCAN_PATH=$(head -n $i /strm.txt |tail -n 1|tr -d '\r'|cut -f2 -d= |sed 's/\//\\\//g; s/\s\+$//g; s/&/%26/g')
	sed -i "s/DOCKER_ADDRESS/$DOCKER_ADDRESS/" /tmp/strm.py
	sed -i "s/SCAN_PATH/$SCAN_PATH/" /tmp/strm.py
	sed -i "s/USERNAME/$USERNAME/" /tmp/strm.py
	sed -i "s/PASSWORD/$PASSWORD/" /tmp/strm.py
	/tmp/strm.py
    k=$(head -n $i /strm.txt |tail -n 1|tr -d '\r'|cut -f2 -d= |sed 's/\s\+$//g; s/%20/ /g; s/&/%26/g')
	cd /media/strm"$k"
    fd --extension strm --exec sed \-i "s# #%20#g; s#|#%7C#g" {} \; 
	#find /media/strm"$k" -name "*.strm" -exec sed \-i "s# #%20#g; s#|#%7C#g" {} \;
	chmod -R 777 /media/strm"$k"/*
done
