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
    # dmap = np.fromstring(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)  # Works & It's FAST
    dmap = np.frombuffer(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)  # Works & It's FAST

    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = cv.cvtColor(d4d,cv.COLOR_GRAY2RGB)
    # Shown unknowns in black
    # d4d = 255 - d4d
    return dmap, d4d



def get_contours(img):
    print("getcontours")
    print("img= " + str(img.dtype))
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # print("gray= " + str(gray.dtype))
    # thresh = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    # print("tresh= " + str(thresh.dtype))
    # img = cv.cvtColor(img,cv.COLOR_GRAY2RGB)
    
    # ret, bin_img = cv.threshold(img, 23, 255, cv.THRESH_BINARY)


    # cnts = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # cnts = sorted(cnts, key=cv.contourArea, reverse=True)
    # for c in cnts:
    #     # print (i, c)
    #     # Highlight largest contour
    #     cv.drawContours(img, [c], -1, (36,255,12), 3)
    #     # break
    return img
    # return thresh

detector = cv.SimpleBlobDetector()

def get_blobs(img, detector):
    keypoints = detector.detect(img)
    im_with_keypoints = cv.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return im_with_keypoints

def line(img, start, end):
    thickness = 2
    line_type = 8
    cv.line(img,start,end,(0, 255, 0),thickness,line_type)

def redline(img, start, end):
    thickness = 2
    line_type = 8
    cv.line(img,start,end,(0, 0, 255),thickness,line_type)





backdepth, backimg = get_depth()
# backdepth = backdepth.astype(np.int16)
# backimg = backimg.astype(np.int16)
backbuffer = backdepth.copy()
# print(backdepth)
grayback = cv.cvtColor(backimg,cv.COLOR_BGR2GRAY)


# print(grayback[350])
back_16 = grayback.astype(np.int16)
# print(backimg)









# from matplotlib import pyplot as plt
# # create a list of first 5 frames
# img = [get_depth()[0] for i in range(5)]
# # convert all to grayscale
# # gray = [cv.cvtColor(i, cv.COLOR_BGR2GRAY) for i in img]
# # convert all to float64
# gray = [np.float64(i) for i in img]
# # create a noise of variance 25
# noise = np.random.randn(*gray[1].shape)*10
# # Add this noise to images
# noisy = [i+noise for i in gray]
# # Convert back to uint8
# noisy = [np.uint8(np.clip(i,0,255)) for i in noisy]
# # Denoise 3rd frame considering all the 5 frames
# dst = cv.fastNlMeansDenoisingMulti(noisy, 2, 5, None, 4, 7, 35)
# dst = dst.astype(np.int16)
# # plt.subplot(131),plt.imshow(gray[2],'gray')
# # plt.subplot(132),plt.imshow(noisy[2],'gray')
# # plt.subplot(133),plt.imshow(dst,'gray')
# # plt.show()


# dmap,frame = get_depth()

# # print(dmap.size)

# frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
# frame_16 = frame.astype(np.int16)
# sframe_16 = np.subtract(back_16, frame_16)
# # print(sframe_16[350])
# sframe_16 = abs(sframe_16)
# sframe = sframe_16.astype(np.int8)
# # print(sframe[350])

counter = 0


while(1):
    # ret, frame = cap.read()
    dmap,frame = get_depth()
    print ('Center pixel is {}mm away'.format(dmap[239,319]))
    print ('backgroundCenter pixel is {}mm away'.format(backbuffer[239,319]))
    deltamap = cv.subtract(backbuffer,dmap)  
    # if counter%10 == 0:
    #     print(dmap.dtype)
    #     print(backdepth.dtype)
    #     print (counter)
    #     print(deltamap)
    # counter = counter +1

    # frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    # frame =frame.astype(np.int16)
    # dmap = dmap.astype(np.int16)
    # # fgframe = dmap - dst
    # # fgframe = backdepth - dmap
    # fgframe = np.subtract(backdepth ,dmap)
    # # frame = frame - backimg
    # frame = np.subtract(frame,backimg)
    # print(frame[350])
    # frame = frame - greyback
    # print(frame[350])
    # cv.imshow('frameD',dmap)
    # cv.imshow('frameW',frame)
    # frame = np.where(frame > 150, 0, 255)
    # frame = frame.astype(np.int16)

    frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    frame_16 = frame.astype(np.int16)
    sframe_16 = np.subtract(back_16, frame_16)
    # print(sframe_16[350])
    sframe_16 = abs(sframe_16)
    
    
    ### this
    # img8 = (sframe_16/256).astype('uint8')
    # result = (img8 > 25 ) * img8

    ### or this
    
    
    sframe = sframe_16.astype(np.int8)
    
    result = (sframe > 10 ) * sframe
    result = result.astype(np.float32)
    
    # cont = cv.cvtColor(result,cv.COLOR_GRAY2RGB)

    # print(np.count_nonzero(result, axis=1))
    hotrows = (np.count_nonzero(result, axis=1) > 30)
    hotrows = (np.count_nonzero(result, axis=1) < 100) 
    # print (hotrows)
    detpoints = np.zeros((480, 640, 3), dtype=np.uint8)
    regions = []


    for i,row in enumerate(hotrows):
        regions.append([])
        if (row == False):
            a = np.nonzero(result[i])
            # print(a[0][]0)
            start = a[0][0]
            end = a[0][-1]
            width = 0
            count = 0
            
            for j,k in enumerate(a[0][:-1]):
                if (k + 1 == a[0][j+1]):
                    if (width == 0):
                        # regions.append[k]
                        start = k
                        width = width + 1
                        # print(width)
                    else:
                        width = width + 1

                else:
                    if (width > 4):  ### threshold for regions
                        # regions.append(a[0][j-1])
                        end = a[0][j-1]
                        if (end-start < 50 and end-start > 10 and i < 320):
                            regions[i].append((start,end))
                        # width = 0
                        # regions = regions[:-1].copy()
                    # else:
                    width = 0
                    count += count

            # print(start,end)
            # if (i > 
            
            for r in regions[i]:
                x = int(((r[0]+r[1])/2))
                # if (i == 300):
                # print(x)
                if (deltamap[i][x] < 100 ):
                    # print(deltamap[i][x])
                    redline(detpoints, (r[0],i), (r[1],i))
                else:
                    line(detpoints, (r[0],i), (r[1],i))
    # for i,row in enumerate(regions[:-1]):
    #     if row:
    #         for line in row:
    #             # if (line[0] - row[i+1]




    # for row in hotrows:
        # print (row)


    # print(result[350])
    # ret,sframe = cv.threshold(sframe,140,255,cv.THRESH_TOZERO_INV)
    # print(result[350])
    # ret, bin_img = cv.threshold(result, 127, 255, cv.THRESH_BINARY)


    # cont = get_contours(result)
    # blobs = get_blobs(result,detector) ### crash


    cv.imshow('frame', result)
    cv.imshow('framedet', detpoints)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break


## Release resources 
cv.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")
