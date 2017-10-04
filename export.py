from shutil import copyfile
import os
import numpy as np
import piezas as ps
import PIL.Image
import scipy.misc


from argparse import ArgumentParser

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s');

PATHDATASET = 'db';
NAMEANOTATION = 'anotation'
NAMEDATASET = 'v001'
PATHOUTPUT = 'out'


def bboxadjust(bbox, aspX=1.0, aspY=1.0, minX=0.0, minY=0.0):          
    '''
    BBox adjust
    '''
    bbox[:,0] = bbox[:,0]*(1/aspX)  + minX;
    bbox[:,1] = bbox[:,1]*(1/aspY)  + minY;
    return bbox;

def adjustdata(image, labels, border=0, shapein=(1080, 1920), shapeout=(640,1024)):
    '''
    Adjustdata
    '''
    
    W=shapein[1]; H=shapein[0]; 
    h,w,c = image.shape;
    h = float(h); 
    w = float(w);
     
    #-----
    aspY=H/h; aspX=W/w;
    im = scipy.misc.imresize(image, (H, W), interp='bilinear')    
    
    #-----
    asp=float(shapeout[1])/float(shapeout[0]);
    H1= int(H-border); W1 = int(H1*asp)
    Hdif=int(np.abs(H-H1)/2.0); Wdif=int(np.abs(W-W1)/2.0)
    vbox = np.array([[Wdif,Hdif],[W-Wdif,H-Hdif]]); 
    
    imp = im[vbox[0,1]:vbox[1,1],vbox[0,0]:vbox[1,0],:];
    aspYp =  float(shapeout[0])/imp.shape[0];
    aspXp =  float(shapeout[1])/imp.shape[1];
    
    impp = scipy.misc.imresize(imp, (shapeout[0], shapeout[1]), interp='bilinear') 
    labelpp = list();
    for l in labels:
        l.bbox = bboxadjust(l.bbox, 1/aspX , 1/aspY, -vbox[0,0], -vbox[0,1]) 
        l.bbox = bboxadjust(l.bbox, 1/aspXp, 1/aspYp)
        labelpp.append(l);
    
    return impp, labelpp;


def mse(Ia, Ib):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((Ia.astype("float") - Ib.astype("float")) ** 2)
    err /= float(Ia.shape[0] * Ia.shape[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def vatic2kitti( pathannotation, pathout, namedata, skip=10, maxerr=20):
    '''
    Vatic to kitti
    '''
      
    # Create output struct folders 
    pathnamenamedata = os.path.join(pathout,namedata);
    pathname_image = os.path.join(pathnamenamedata, 'images');
    pathname_label = os.path.join(pathnamenamedata, 'labels');

    if os.path.exists(pathnamenamedata) is not True:
        os.makedirs(pathnamenamedata);
        os.makedirs(pathname_image);
        os.makedirs(pathname_label);    

    annotation=[]; names=[];
    with open( os.path.join(pathannotation,'{}.txt'.format(namedata)), "r" ) as f:
        for line in f:  
            try: 
                fields=line.split(' ')
                if fields[6]!='1' and fields[7]!='1':
                    annotation.append([int(fields[5]), int(fields[1]), int(fields[2]), int(fields[3]), int(fields[4])])
                    names.append(fields[9][1:-2])
            except IndexError as e:
                print('Error format: {}'.format(e))
              
    annotation=np.asarray(annotation)
    frame=np.unique(annotation[:,0])
    
    i=0;
    image_old = np.empty((640,1024,3));
    for num_frame in frame:

        if (i+1)%skip == 0: i+=1; continue;
        
        subfolder = num_frame//100
        folder = subfolder//100

        path_image = os.path.join( pathannotation, namedata, str(folder), str(subfolder), '{}.jpg'.format(num_frame) )
        image = PIL.Image.open(path_image)
        image.load()
        image = np.array(image);
                       
        
        # select
        index=np.where(annotation[:,0]==num_frame)[0]
        labels= list();
        for num_piece in index:
            piece = ps.Piece()
            minr, minc, maxr, maxc = annotation[num_piece,1:5]
            piece.bbox = np.array([[minr,minc],[maxr,maxc]]) 
            piece.truncation = False
            piece.stype = names[num_piece]
            l = ps.DetectionGT()
            l.assignment(piece)
            labels.append(l);
       

        # ajust image and label
        image, labels = adjustdata(image, labels);  

        # filter
        if i==0: image_old=image;
        if mse(image, image_old)<maxerr: i+=1; continue;
        image_old = image;
                 
        
        # create label  
        with open(os.path.join(pathname_label, '{:06d}.txt'.format(i)), 'w') as f:
            for l in labels:
                li = l.gt_to_kitti_format();                
                f.write('{} '.format(li[0]));
                f.write('{} '.format(li[1]));
                f.write('{} '.format(li[2]));
                for e in range(3,15):
                    f.write('{:.2f} '.format(li[e]));
                f.write('\n');
        
        # create image 
        scipy.misc.imsave(os.path.join(pathname_image, '{:06d}.png'.format(i)), image);        
        #copyfile(path_image, os.path.join(pathname_image,'{:06d}.jpg'.format(num_frame) ))      
        
        logging.info('image procces {:06d}'.format( i ));
        i+=1;




def arg_parser():
    
    parser = ArgumentParser();    
    parser.add_argument('--pathdataset',
            dest='pathdataset', help='path dataset',
            required=True, metavar='s', default=PATHDATASET)
    parser.add_argument('--anotation',
            dest='nameanotation', help='name anotation',
            required=True, metavar='s', default=NAMEANOTATION)
    parser.add_argument('--name',
            dest='namedata', help='name video',
            required=True, metavar='s', default=NAMEDATASET)
    parser.add_argument('--output',
            dest='pathoutput', help='path output',
            required=True, metavar='s', default=PATHOUTPUT)

    return parser;


if __name__ == '__main__':
     
    parser = arg_parser();
    options = parser.parse_args();
    
    pathdataset = options.pathdataset;
    pathanotation = os.path.join(pathdataset, options.nameanotation);
    namedata = options.namedata;
    pathoutput  = options.pathoutput; 
    

    vatic2kitti( pathanotation, pathoutput, namedata )




