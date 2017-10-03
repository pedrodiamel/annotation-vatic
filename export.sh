#!/bin/bash

PATHDATASET='db';
NAMEANOTATION='anotation';
NAMEDATASET='v00xxx';
PATHOUTPUT='/home/pdmf/docker/caffe/visualkit/db/Local';

python export.py \
--pathdataset=$PATHDATASET \
--anotation=$NAMEANOTATION \
--name=$NAMEDATASET \
--output=$PATHOUTPUT \



