import numpy as np
import cv2
from primesense import openni2#, nite2
from primesense import _openni2 as c_api

# dist ='/home/pi/'
dist = 'OpenNI-MacOSX-x64-2.2/Redist/' ## MACOSX
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
    d4d = cv2.cvtColor(d4d,cv2.COLOR_GRAY2RGB)
    # Shown unknowns in black
    d4d = 255 - d4d
    return dmap, d4d

## get background image
backdepth, backimg = get_depth()

print("backimg =" + str(backimg.dtype))
gray = cv2.cvtColor(backimg, cv2.COLOR_BGR2GRAY)
print("gray =" + str(gray.dtype))
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
print("tresh= " + str(thresh.dtype))
# Find contours and sort using contour area
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
for c in cnts:
    # print (i, c)
    # Highlight largest contour
    cv2.drawContours(backimg, [c], -1, (36,255,12), 3)
    # break




cv2.imshow('thresh', thresh)
cv2.imshow('image', backimg)
cv2.waitKey()

