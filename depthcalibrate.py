## this file can be used for calibration, saving depth buffers
## if objects are moved in the room, recalibrate using this file!

## buffer will first be saved after 10 seconds, so you have time to move out of view
# change " unimportandfilenametonotoverwriteimportantones" to something sensible at line 68


import numpy as np
import cv2 as cv
from pythonosc import udp_client
client = udp_client.SimpleUDPClient("127.0.0.1", 9002) #PD client
blender = udp_client.SimpleUDPClient("127.0.0.1", 9001) #blender client
waves = {}
from primesense import openni2#, nite2
from primesense import _openni2 as c_api


import pickle
import time

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


time.sleep(10)

backdepth, backimg = get_depth()
backbuffer = backdepth.copy()
backimgbuffer = backimg.copy()



filename = 'homebackbuffer.pickle'
outfile = open(filename,'wb')
pickle.dump(backdepth,outfile)
outfile.close()


# filename = 'backimgwith4feet.pickle'
# outfile = open(filename,'wb')
# pickle.dump(backimg,outfile)
# outfile.close()





counter = 0


# Setup SimpleBlobDetector parameters.
params = cv.SimpleBlobDetector_Params()
# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200
#filter by color
# params.filterByColor = True 
# blobColor = 255
# Filter by Area.
# params.filterByArea = True
# params.minArea = 1200
# # Filter by Circularity
# params.filterByCircularity = True
# params.minCircularity = 0.1
# # Filter by Convexity
# params.filterByConvexity = True
# params.minConvexity = 0.87
# # Filter by Inertia
# params.filterByInertia = True
# params.minInertiaRatio = 0.01
# params.maxInertiaRatio = 1
detector = cv.SimpleBlobDetector_create(params)


while(1):
    # ret, frame = cap.read()
    dmap,frame = get_depth()
    
    deltamap = cv.subtract(backbuffer,dmap)
    
    # print (deltamap.dtype)
    # closemap = [x < 10] * deltamap

    buffer = (deltamap > 15) * deltamap 
    buffer = (buffer < 150) * deltamap
    result = cv.normalize(buffer, buffer, 0, 255, cv.NORM_MINMAX)
    cv.imshow('buffer', backimgbuffer)
    
    result = cv.normalize(buffer, buffer, 0, 255, cv.NORM_MINMAX)
    # result = result.astype(np.uint8)
    result = (result  < 150 ) * result
    result[result != 0] = 128
    
    # # result = (result < 50 )
    # deltamap = deltamap.astype(np.uint8)
    # print (result.dtype)
    # result.astype(np.uint8)
    
    result = (result > 55)
    result = result.astype(np.uint8)
    result[result != 0] = 255
    kernel = np.ones((3,3), np.uint8)       # set kernel as 3x3 matrix from numpy
    #Create erosion and dilation image from the original image
    erosion = cv.erode(result, kernel, iterations=1)







    # print (result.dtype)
    # result[result == True] = 255
    # result.astype(np.uint8)
    detpoints = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # detpoints[x,y]=[255, 255, 255]
    # zeros = np.zeros(detpoints.shape[:2], dtype="uint8")
    # cv.imshow("Red", cv.merge([zeros, zeros, result]))
    # cv.imshow('frame', erosion)
    inv = cv.bitwise_not(erosion)

    # findcontours 
    cnts = cv.findContours(inv, cv.RETR_LIST, 
                    cv.CHAIN_APPROX_SIMPLE)[-2] 

    # filter by area 
    s1 = 200
    s2 = 4000
    xcnts = [] 
    for i,cnt in enumerate(cnts): 
        # print(cv.contourArea(cnt))
        if s1<cv.contourArea(cnt) <s2: 
            xcnts.append(cnt)
            M = cv.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # print(cX,cY)
            if ("wave"+str(i) in waves):
                if (waves["wave"+str(i)][0] - cX > 10 or waves["wave"+str(i)][1] - cY > 10 ): #moved too much, give new wave
                    blender.send_message("/wave"+ str(i) , 1)
                    client.send_message("/wave"+ str(i) , 1)

            else:
                waves["wave"+str(i)] = (cX,cY)
                blender.send_message("/wave"+ str(i) , 1)
                client.send_message("/wave"+ str(i) , 1)

            client.send_message("/cnt"+ str(i) +"/cX", cX)
            client.send_message("/cnt"+ str(i) +"/cY", cY)
            CX = cX/640 * 6 - 3
            CY = cY/480 * 4 - 2
            blender.send_message("/wave"+ str(i) +"/cX", CX)
            blender.send_message("/wave"+ str(i) +"/cY", CY)

    keypoints = detector.detect(inv)

    # # Draw detected blobs as red circles.
    # # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv.drawKeypoints(inv, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # # Show keypoints
    # cv.imshow("Keypoints", im_with_keypoints)

    # if (counter % 20 == 0):
    # # #     print ('Center pixel is {}mm away'.format(dmap[239,319]))
    # # #     print ('backgroundCenter pixel is {}mm away'.format(backbuffer[239,319]))
    # #     # print ('DeltaCenter pixel is {}mm away'.format(deltamap[239,319]))
    # #     # print ('result pixel is {}mm away'.format(result[239,319]))
    # #     # print(result)
    #     # print(keypoints)
    #     print (len(xcnts))
    counter = counter + 1

    if (counter == 100):
        filename = 'home.pickle'
        outfile = open(filename,'wb')
        pickle.dump(dmap,outfile)
        outfile.close()
        print("saved dmap frame after " + str(counter) + "frames")

    k = cv.waitKey(30) & 0xff
    if k == 27:
        break


## Release resources 
cv.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")



    