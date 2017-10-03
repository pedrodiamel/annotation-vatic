# [Vatic](http://carlvondrick.com/vatic/) for detectNet annotation

Herramienta para generar datos para el entrenamiento de la red [detectNet](hwtps://github.com/NVIDIA/DIGITS/tree/master/examples/object-detection).


### INSTALLATION

- [Installation instruction]( https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)
- [Easy installation deb file]( https://download.docker.com/linux/ubuntu/dists/)


### ANNOTATION

1- Install annotation server

    bash install.sh

2- Copy videos: copy your videos on data folder

3- Execute annotation server

    bash exec.sh

4- Click on links in the screen

5- Make annotation

6- Save annotation

    bash save.sh

### EXPORT

1- Export for detectNet format

    python export.py

### FEEDBACK AND BUGS

Please direct all comments and report all bugs to:

- Pedro D. Marrero Fernandez: pdmf@cin.ufpe.br
- Fidel A. Guerrero Peña: fagp@cin.ufpe.br

Thanks for using our system!