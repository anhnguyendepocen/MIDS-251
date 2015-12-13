#!/bin/bash

while read -r line; do
	echo "Getting file $line ..."
	swift download reddit $line
	echo "Decompressing $line ..."
	bzip2 -d $line
	echo "Uploading decompressed file ${line%.*}"
	swift upload reddit2 ${line%.*} -S 1073741824;
	echo "Deleting decompressed file ${line%.*}"
	rm -rf ${line%.*}
done < "$1"

