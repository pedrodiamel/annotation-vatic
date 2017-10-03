#!/bin/bash
FILES=/home/vagrant/vagrant_data/*.mp4
labels="`cat /home/vagrant/vagrant_data/config/labels.txt`"
for f in $FILES
do
filename=$(basename "$f")
filename="${filename%.*}"
turkic extract $f /home/vagrant/vagrant_data/$filename --no-resize
done


id=0

for f in $FILES
do
filename=$(basename "$f")
filename="${filename%.*}"
turkic load $id /home/vagrant/vagrant_data/$filename $labels --offline --length 4000
id=$((id + 1)) 
done
echo ""
echo ""
echo "Open in browser"
turkic publish --offline

