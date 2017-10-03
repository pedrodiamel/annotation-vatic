#!/bin/bash
cd /home/vagrant/vatic
FILES=/home/vagrant/vagrant_data/*.mp4
id=0

for f in $FILES
do
filename=$(basename "$f")
filename="${filename%.*}"
turkic dump $id -o /home/vagrant/vagrant_data/${filename}.txt
turkic delete $id --force
id=$((id + 1)) 
done

