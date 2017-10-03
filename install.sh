DATA_DIR=`pwd`

sudo docker pull jldowns/vatic-docker-contrib:0.1
sudo docker run -d -p 8181:80 -v $DATA_DIR:/home/vagrant/vagrant_data --name vatic  jldowns/vatic-docker-contrib:0.1 tail -f /dev/null

sudo docker cp $DATA_DIR/config/bashrc vatic:/home/vagrant/.bashrc
