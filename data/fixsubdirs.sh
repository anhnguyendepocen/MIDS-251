#!/bin/bash

year="2011"
for i in "authorperday_counts" "subreddit_counts" "time_counts" "counts_all"
do
  cd ~/Development/MIDS-251/data/$year/$i
  mv $i ../_$i
  cd ..
  rm -rf $i
  mv _$i $i
done
