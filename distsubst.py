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



backdepth, backimg = get_depth()
# backdepth = backdepth.astype(np.int16)
# backimg = backimg.astype(np.int16)


grayback = cv.cvtColor(backimg,cv.COLOR_BGR2GRAY)


print(grayback[350])
back_16 = grayback.astype(np.int16)
# print(backimg)









from matplotlib import pyplot as plt
# create a list of first 5 frames
img = [get_depth()[0] for i in range(5)]
# convert all to grayscale
# gray = [cv.cvtColor(i, cv.COLOR_BGR2GRAY) for i in img]
# convert all to float64
gray = [np.float64(i) for i in img]
# create a noise of variance 25
noise = np.random.randn(*gray[1].shape)*10
# Add this noise to images
noisy = [i+noise for i in gray]
# Convert back to uint8
noisy = [np.uint8(np.clip(i,0,255)) for i in noisy]
# Denoise 3rd frame considering all the 5 frames
dst = cv.fastNlMeansDenoisingMulti(noisy, 2, 5, None, 4, 7, 35)
dst = dst.astype(np.int16)
# plt.subplot(131),plt.imshow(gray[2],'gray')
# plt.subplot(132),plt.imshow(noisy[2],'gray')
# plt.subplot(133),plt.imshow(dst,'gray')
# plt.show()


dmap,frame = get_depth()

frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
frame_16 = frame.astype(np.int16)
sframe_16 = np.subtract(back_16, frame_16)
print(sframe_16[350])
sframe_16 = abs(sframe_16)
sframe = sframe_16.astype(np.int8)
print(sframe[350])



while(1):
    # ret, frame = cap.read()
    dmap,frame = get_depth()

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
    sframe_16 = abs(sframe_16)
    sframe = sframe_16.astype(np.int8)
    result = (sframe > 25 ) * sframe
    print(result[350])
    # ret,sframe = cv.threshold(sframe,140,255,cv.THRESH_TOZERO_INV)

    cv.imshow('frame',result)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break


## Release resources 
cv.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")
