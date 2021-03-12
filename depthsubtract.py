import numpy as np
import cv2 as cv
from primesense import openni2#, nite2
from primesense import _openni2 as c_api

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





def get_depth():
    dmap = np.frombuffer(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)  # Works & It's FAST
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = cv.cvtColor(d4d,cv.COLOR_GRAY2RGB)
    # Shown unknowns in black
    d4d = 255 - d4d
    return dmap, d4d


def redline(img, start, end):
    thickness = 2
    line_type = 8
    cv.line(img,start,end,(0, 0, 255),thickness,line_type)


backdepth, backimg = get_depth()

backbuffer = backdepth.copy()

counter = 0

while(1):
    # ret, frame = cap.read()
    dmap,frame = get_depth()
    
    deltamap = cv.subtract(backbuffer,dmap)
    # print (deltamap.dtype)
    # closemap = [x < 10] * deltamap

    buffer = (deltamap > 30) * deltamap 
    buffer = (buffer < 150) * deltamap
    # result = (result  < 150 ) * result
    result = cv.normalize(buffer, buffer, 0, 255, cv.NORM_MINMAX)
    result = result.astype(np.uint8)
    # result[result != 0] = 128
    # # result = (result < 50 )
    # deltamap = deltamap.astype(np.uint8)
    # print (result.dtype)
    # result.astype(np.uint8)
    result = (result > 150)
    result = result.astype(np.uint8)
    result[result != 0] = 255
    # print (result.dtype)
    # result[result == True] = 255
    # result.astype(np.uint8)
    detpoints = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # detpoints[x,y]=[255, 255, 255]
    # zeros = np.zeros(detpoints.shape[:2], dtype="uint8")
    # cv.imshow("Red", cv.merge([zeros, zeros, result]))
    cv.imshow('frame', result)


    if (counter % 20 == 0):
    #     print ('Center pixel is {}mm away'.format(dmap[239,319]))
    #     print ('backgroundCenter pixel is {}mm away'.format(backbuffer[239,319]))
        print ('DeltaCenter pixel is {}mm away'.format(deltamap[239,319]))
        print ('result pixel is {}mm away'.format(result[239,319]))
        # print(result)
    counter = counter + 1


    k = cv.waitKey(30) & 0xff
    if k == 27:
        break


## Release resources 
cv.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")



    