import numpy as np
import cv2 as cv
from primesense import openni2#, nite2
from primesense import _openni2 as c_api

dist ='lib'
openni2.initialize(dist) #
if (openni2.is_initialized()):
    print ("openNI2 initialized")
else:
    print ("openNI2 not initialized")

## Register the device
dev = openni2.Device.open_any()
dev.set_depth_color_sync_enabled('enable')
depth_stream = dev.create_depth_stream()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=640, resolutionY=480, fps=30))
depth_stream.set_mirroring_enabled(False)
depth_stream.start()


def get_depth():
    dmap = np.fromstring(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)  # Works & It's FAST
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = cv.cvtColor(d4d,cv.COLOR_GRAY2RGB)
    # Shown unknowns in black
    d4d = 255 - d4d
    return dmap, d4d

## get background image
# backdepth, backimg = get_depth()


# cap = cv.VideoCapture('vtest.avi')
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
fgbg = cv.bgsegm.createBackgroundSubtractorGMG()

while(1):
    # ret, frame = cap.read()
    dmap,frame = get_depth()
    fgmask = fgbg.apply(frame)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)    
    cv.imshow('frame',fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break


## Release resources 
cv.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")