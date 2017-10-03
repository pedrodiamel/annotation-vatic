sudo docker exec -ti vatic bash /home/vagrant/vagrant_data/config/save.bash

mkdir send

FILES=*.mp4
for f in $FILES
do
filename=$(basename "$f")
filename="${filename%.*}"
cp -rf $filename send/$filename
cp -rf ${filename}.txt send/${filename}.txt
sudo rm -rf $filename
sudo rm -rf ${filename}.txt
done
