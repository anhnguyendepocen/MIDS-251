#!/bin/bash
STARTTIME=$(date +%s)
while read -r line; do
	echo "Getting file $line ..."
	swift download reddit2 $line
	dirName=${line::4}
	fileName=${line:5}
	cd $dirName
	echo "Uploading file ${fileName%.*}"
	swift upload reddit3 ${fileName%.*} -S 1073741824;
	cd ..
	echo "Deleting file ${fileName%.*}"
	rm -rf ${line%.*}
done < "$1"
ENDTIME=$(date +%s)
echo "Completed in $(($ENDTIME - $STARTTIME)) seconds"
