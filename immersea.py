#### DO SOME CONFIG BELOW

import numpy as np
import cv2 as cv
from pythonosc import udp_client
from pythonosc import osc_message_builder  ### to be able to sned multiple parameters

from primesense import openni2#, nite2
from primesense import _openni2 as c_api
import time
import rtmidi
from rtmidi.midiutil import open_midiinput

midiout = rtmidi.MidiOut()
midiin = rtmidi.MidiIn()
available_out_ports = midiout.get_ports()
available_in_ports = midiin.get_ports()
print("out:" + str(available_out_ports))
print("in" + str(available_in_ports))



## camera config, using structure.io
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


### CONFIG HERE
startupdelay = 5 ## how long before a backbuffercopy is made (if you need time to move out of the camera view when starting, do it here)
# image cut, see below search for cut_image
cutY = 0
## detection parameters, tweak and copy to immersea.py
minD = 200  ### minimum distance to consider close to ground (not to low, or you will pickup a lot of noise) (dflt = 500)
maxD = 400  ### maximum distance (dflt = 800) minD needs to be smaller than maxD
cntrMin = 200 ### minimum contourSize to consider as a blob (dflt = 100)
cntrMax = 20000 ###  minimum contourSize to consider as a blob (dflt = 600)

## experience parameters
wigglespace = 5 #how much can you move your foot before a new note is sent
waves = {}
lastfeet = []
stage = 0 ## startstage, change to do debugging, 0 == idle
shutdowntimeout = 10 ## if no foot has been seen for shutdowntimeout seconds, switch to stage 0
stage1time = 50 #how long does stage 1 take in seconds?
stage2time = stage1time + 5
stage3time = stage2time + 5


## comunication config
# client = udp_client.SimpleUDPClient("127.0.0.1", 9002) #PD client
# blender = udp_client.SimpleUDPClient("127.0.0.1", 9001) #blender client
processing = udp_client.SimpleUDPClient("127.0.0.1", 12000) #processing client


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        # self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        # self._wallclock += deltatime
        # print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        
        if (message[1] == 2) :
            minD = 20 + 3*(message[2])
            stage = int(message[2]/12)
            print("stage =" + str(stage))
            processing.send_message("/stage", stage)
        if (message[1] == 3) :
            maxD = 100 + 5*(message[2])
            print("maxD =" + str(maxD))
        
        





def getDepth():
    dmap = np.frombuffer(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)  # Works & It's FAST
    return dmap

def testDepth():
    deltamap = cv.subtract(backbuffer,dmap)
    buffer = (deltamap > minD) * deltamap 
    buffer = (buffer < maxD) * buffer   
    cvuint8 = cv.convertScaleAbs(buffer)
    cnts = cv.findContours(cvuint8, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[-2]
    s1 = cntrMin
    s2 = cntrMax
    xcnts = []
    feet = []
    for i,cnt in enumerate(cnts): 
        if s1<cv.contourArea(cnt) <s2: 
            xcnts.append(cnt)
            M = cv.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #add to "feet"
            feet.append((cX,cY))
    # print(feet)
    return feet

def processFeet(feet):
    global lastfeet
    global wigglespace
    newmask = []
    gonemask = []
    #feet gone?
    # if len(lastfeet) > 0:
    #     footGone = True
    #     for i,lf in enumerate(lastfeet):
    #         if len(lastfeet) > 0:
    #             for f in feet:
    #                 if ( ((lf[0] - f[0]) < wigglespace) and ((lf[1] - f[1]) < wigglespace) ):
    #                     footGone = False
    #     if footGone:
    #         print("foot" +str(i) + "has left the building" + str(lf[0]) + "," + str(lf[1]))

    # more than 0 feet?
    if len(feet) > 0:
    #new feet?
        for i,f in enumerate(feet):
            # newmask.append(False)
            newFound = True
            if len(lastfeet) > 0:
                for lf in lastfeet:
                    if ( ((lf[0] - f[0]) < wigglespace) and ((lf[1] - f[1]) < wigglespace) ):
                        newFound = False
            if newFound:
                # print("new " +str(i) + " found" + str(f[0]) + "," + str(f[1]))
                note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
                midiout.send_message(note_on)
                processing.send_message("/foot", [f[0], f[1]])
                

    lastfeet = feet

# def processDepth():
#     ## unstretch X factor
    

if available_out_ports:
    # midiout, port_name = open_midioutput(3)
    midiout.open_port(2)
else:
    midiout.open_virtual_port("My virtual output")

if available_in_ports:
    midiin, port_name = open_midiinput(3)
    print("Attaching MIDI input callback handler.")
    midiin.set_callback(MidiInputHandler(port_name))
else:
    midiin.open_virtual_port("My virtual input")



# set delay for backgroud image (move out of the way!!!)
time.sleep(startupdelay)
backdepth = getDepth()
backbuffer = backdepth.copy()
counter = 0
starttime = time.time() ## time the cycle is first started.
feettime = starttime

while(1):
    if (len(lastfeet) == 0 and stage != 0):
        #check how long it has been zero
        zerotime = time.time() - feettime
        if (zerotime > shutdowntimeout):
            stage = 0 ## shut down the experience
            processing.send_message("/stage", 0)
    if (len(lastfeet) !=0):
        feettime = time.time() 
    if (stage == 0 and len(lastfeet) !=0):
        starttime = time.time()
        stage = 1
        processing.send_message("/stage", 1)
    if ( ((time.time() - starttime) > stage1time) and stage == 1 ) :
        stage = 2
        processing.send_message("/stage", 2)
    if ( ((time.time() - starttime) > stage2time) and stage == 2 ) :
        stage = 3
        processing.send_message("/stage", 3)
    if ( ((time.time() - starttime) > stage3time) and stage == 3 ) :
        stage = 4
        processing.send_message("/stage", 4)

    dmap = getDepth()
    processFeet(testDepth())
    # print(feettime, starttime)

    k = cv.waitKey(30) & 0xff
    if k == 27:
        break


## Release resources
midiout.close_port()
del midiout
midiin.close_port()
del midiin
cv.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")
