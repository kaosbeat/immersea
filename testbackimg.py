## calibration parameters
## STEP 1 read comments!
# image cut, see below search for cut_image
cutY = 100
## test offline (0) or with camera (1)
test = 1

## detection parameters, tweak and copy to immersea.py
minD = 150  ### minimum distance to consider close to ground (not to low, or you will pickup a lot of noise) (dflt = 500)
maxD = 400  ### maximum distance (dflt = 800) minD needs to be smaller than maxD

cntrMin = 500 ### minimum contourSize to consider as a blob (dflt = 100)
cntrMax = 20000 ### minimum contourSize to consider as a blob (dflt = 600)


# copy these to the immerse file!
## end of configuration


from pythonosc import udp_client
from primesense import openni2#, nite2
from primesense import _openni2 as c_api
import numpy as np
import cv2 as cv
import pickle



filename = 'backdepth.pickle'
infile = open(filename,'rb')
backdepth = pickle.load(infile)
infile.close()

filename = 'backimg.pickle'
infile = open(filename,'rb')
backimg = pickle.load(infile)
infile.close()

filename = "backwith2feet.pickle"
infile = open(filename,'rb')
backwith2feet = pickle.load(infile)
infile.close()

filename = "backimgwith2feet.pickle"
infile = open(filename,'rb')
backimgwith2feet = pickle.load(infile)
infile.close()

filename = "backwith4feet.pickle"
infile = open(filename,'rb')
backwith4feet = pickle.load(infile)
infile.close()

filename = "backimgwith4feet.pickle"
infile = open(filename,'rb')
backimgwith4feet = pickle.load(infile)
infile.close()

filename = "after100frames.pickle"
infile = open(filename,'rb')
after100frames = pickle.load(infile)
infile.close()

# cut, only consider pixels in this cut
cut_image = backimgwith4feet[cutY: 480, 0: 640] # add the cut parameters in the getDepth function below
cv.imshow('cut', cut_image)

# add the cut parameters in the function below
def getDepth():
    dmap = np.frombuffer(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)  # Works & It's FAST
    dmap = dmap[cutY: 480, 0: 640]
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = cv.cvtColor(d4d,cv.COLOR_GRAY2RGB)
    # Shown unknowns in black
    d4d = 255 - d4d
    return dmap, d4d


if test == 0:
    backbuffer = backdepth[cutY: 480, 0: 640]
    dmap = backwith4feet[cutY: 480, 0: 640]

if test == 1:
    # dist ='lib' ##RPi
    dist = 'OpenNI-MacOSX-x64-2.2/Redist/' ## MACOSX
    openni2.initialize(dist) #
    if (openni2.is_initialized()):
        print ("openNI2 initialized")
    else:
        print ("openNI2 not initialized")

    ## Register the device
    dev = openni2.Device.open_any()
    # dev.set_depth_color_sync_enabled('enable')
    dev.set_depth_color_sync_enabled('disable')

    depth_stream = dev.create_depth_stream()
    depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=640, resolutionY=480, fps=30))
    # depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 640, resolutionY = 480, fps = 30))
    depth_stream.set_mirroring_enabled(False)
    depth_stream.start()
    backdepth, backimg = getDepth()
    backbuffer = backdepth.copy()





# print(cut_image.shape)
# print(backimgwith2feet.shape)
# print(backbuffer.shape)

# add the cut parameters in the function below
def getDepth():
    dmap = np.frombuffer(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)  # Works & It's FAST
    dmap = dmap[cutY: 480, 0: 640]
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = cv.cvtColor(d4d,cv.COLOR_GRAY2RGB)
    # Shown unknowns in black
    d4d = 255 - d4d
    return dmap, d4d

def testDepth():
    deltamap = cv.subtract(backbuffer,dmap)
    # closemap = [x < 10] * deltamap
    buffer = (deltamap > minD) * deltamap 
    buffer = (buffer < maxD) * buffer 
    buffer = buffer*200
    kernel = np.ones((3,3), np.uint8)   # set kernel as 3x3 matrix from numpy
    #Create erosion and dilation image from the original image
    erosion = cv.erode(buffer, kernel, iterations=1)
    # print(erosion.dtype)
    
    cvuint8 = cv.convertScaleAbs(buffer)
    cnts = cv.findContours(cvuint8, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[-2]
    s1 = cntrMin
    s2 = cntrMax
    xcnts = []
    img = emptyImg(cutY)
    for i,cnt in enumerate(cnts): 
        # print(cv.contourArea(cnt))
        if s1<cv.contourArea(cnt) <s2: 
            xcnts.append(cnt)
            M = cv.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            redline(img,(cX,cY),(cX+4,cY+4))
            print(cX,cY) 
    
    cv.imshow('result3', erosion)
    cv.imshow("Red", img)

def redline(img, start, end):
    thickness = 2
    line_type = 8
    cv.line(img,start,end,(0, 0, 255),thickness,line_type)
    

def emptyImg(cutY):
    img = np.zeros((480-cutY, 640, 3), dtype=np.uint8)
    zeros = np.zeros(img.shape[:2], dtype="uint8")
    return img
    # cv.imshow("Red", cv.merge([zeros, zeros, zeros ]))

# testDepth()




while(1):
    if test == 1:
        dmap, frame = getDepth()
        cv.imshow('image', frame)
    testDepth()

    k = cv.waitKey(30) & 0xff
    print(k)
    if k == 27:
        break
    if k == "r":
        print("afeffaafs")