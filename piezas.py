
import numpy as np
import numpy.matlib as matlib
import matplotlib.pyplot as plt  
import utility as utl
import skimage.util as skutl
from scipy.misc import imresize
from scipy.ndimage import rotate as imrotate
import cv2

class ObjectType:
    
    Dontcare, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16 = range(17);
    def __init__(self):
        pass

class DetectionGT:    
    """ 
    This class is the data ground-truth
    """

    # default class mappings
    OBJECT_TYPES = {
        'p1':  ObjectType.p1,
        'p2':  ObjectType.p2,
        'p3':  ObjectType.p3,
        'p4':  ObjectType.p4,
        'p5':  ObjectType.p5,
        'p6':  ObjectType.p6,
        'p7':  ObjectType.p7,
        'p8':  ObjectType.p8,
        'p9':  ObjectType.p9,
        'p10': ObjectType.p10,
        'p11': ObjectType.p11,
        'p12': ObjectType.p12,
        'p13': ObjectType.p13,
        'p14': ObjectType.p14,
        'p15': ObjectType.p15,
        'p16': ObjectType.p16

    }



    def __init__(self):
            self.stype = ''
            self.truncated = 0
            self.occlusion = 0
            self.angle = 0
            self.height = 0
            self.width = 0
            self.length = 0
            self.locx = 0
            self.locy = 0
            self.locz = 0
            self.roty = 0            
            self.bbox = np.zeros((2,2))


    
    def assignment(self, o):

            self.stype = o.stype;
            self.truncated = o.truncation;
            self.occlusion = 0;
            self.angle = 0;
            self.height = 0;
            self.width = 0;
            self.length = 0;
            self.locx = 0;
            self.locy = 0;
            self.locz = 0;
            self.roty = 0;
            self.bbox = o.bbox;
            self.object = self.OBJECT_TYPES.get(o.stype, ObjectType.Dontcare);


    def gt_to_kitti_format(self):
        '''
        Convert to kitti format 
        '''
        result = [

            # set label, truncation, occlusion
            self.stype,
            np.bool(self.truncated).numerator,
            self.occlusion,
            self.angle,
            # set 2D bounding box in 0-based C++ coordinates
            self.bbox[0,0],
            self.bbox[0,1],
            self.bbox[1,0],
            self.bbox[1,1],
            # set 3D bounding box
            self.height,
            self.width,
            self.length,
            self.locx,
            self.locy,
            self.locz, 
            self.roty
        ];
        return result;

    @classmethod
    def lmdb_format_length(cls):
        """
        width of an LMDB datafield returned by the gt_to_lmdb_format function.
        :return:
        """
        return 16

    def gt_to_lmdb_format(self):
        """
        For storage of a bbox ground truth object into a float32 LMDB.
        Sort-by attribute is always the last value in the array.
        """
        result = [
            # bbox in x,y,w,h format:
            self.bbox[0,0],
            self.bbox[0,1],
            self.bbox[1,0] - self.bbox[0,0],
            self.bbox[1,1] - self.bbox[0,1],
            # alpha angle:
            self.angle,
            # class number:
            self.object,
            0,
            # Y axis rotation:
            self.roty,
            # bounding box attributes:
            self.truncated,
            self.occlusion,
            # object dimensions:
            self.length,
            self.width,
            self.height,
            self.locx,
            self.locy,
            # depth (sort-by attribute):
            self.locz,
        ]
        assert(len(result) is self.lmdb_format_length())
        return result



class Piece(object):
    "Piece for mcc generator result"

    stype = '' 
    bbox = np.zeros((4,2));
    truncation = False;


