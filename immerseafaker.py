#### DO SOME CONFIG BELOW
import random
from pythonosc import udp_client
from pythonosc import osc_message_builder  ### to be able to sned multiple parameters

import time
import rtmidi
from rtmidi.midiutil import open_midiinput

midiout = rtmidi.MidiOut()
midiin = rtmidi.MidiIn()
available_out_ports = midiout.get_ports()
available_in_ports = midiin.get_ports()
print("out:" + str(available_out_ports))
print("in" + str(available_in_ports))




### CONFIG HERE
startupdelay = 5 ## how long before a backbuffercopy is made (if you need time to move out of the camera view when starting, do it here)
# image cut, see below search for cut_image
cutY = 100
## detection parameters, tweak and copy to immersea.py
minD = 500  ### minimum distance to consider close to ground (not to low, or you will pickup a lot of noise) (dflt = 500)
maxD = 800  ### maximum distance (dflt = 800) minD needs to be smaller than maxD
cntrMin = 100 ### minimum contourSize to consider as a blob (dflt = 100)
cntrMax = 20000 ###  minimum contourSize to consider as a blob (dflt = 600)

## experience parameters
wigglespace = 15 #how much can you move your foot before a new note is sent
waves = {}

lastfeet = []
stage = 0 ## startstage, change to do debugging, 0 == idle
shutdowntimeout = 10 ## if no foot has been seen for shutdowntimeout seconds, switch to stage 0
stage1time = 120 #how long does stage 1 take in seconds?
stage2time = stage1time + 6 #how long does stage 2 take in seconds?
stage3time = stage2time + 180
stage4time = stage3time + 5
stage5time = stage4time + 180
stage6time = stage5time + 120
opacity = 0 #number of detected steps to fade opacity to 0 at stage 5
sharpen = 1
## comunication config
# client = udp_client.SimpleUDPClient("127.0.0.1", 9002) #PD client
# blender = udp_client.SimpleUDPClient("127.0.0.1", 9001) #blender client
processing = udp_client.SimpleUDPClient("127.0.0.1", 12000) #processing client
millumin = udp_client.SimpleUDPClient("127.0.0.1", 9000) #millumin client
coge = udp_client.SimpleUDPClient("127.0.0.1", 1235) #coge client

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
        
        




def testDepth():
    feet = []
    r = random.randint(0,10)
    n = random.randint(0,4)
    if (r > 2):
        while n > 0:
            cX = random.randint(0,640)
            cY = random.randint(0,380) 
            feet.append((cX,cY))
            n = n-1
    # print(feet)
    return feet

def processFeet(feet):
    global lastfeet
    global wigglespace
    global opacity
    global sharpen

    newmask = []
    gonemask = []
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
                # print("new " +str(i) + " found" + str(f[0]) + "," + str(f[1]) +"stage = " + str(stage))
                if (stage == 1):
                    note = random.randint(60,62)
                    note_on = [0x90, note, 100] # channel 1, middle C, velocity 112
                    midiout.send_message(note_on)
                if (stage == 3):
                    note = random.randint(63,66)
                    note_on = [0x90, note, 100] # channel 1, middle C, velocity 112
                    midiout.send_message(note_on)
                if (stage == 5):
                    note = random.randint(67,72)
                    note_on = [0x90, note, 100] # channel 1, middle C, velocity 112
                    midiout.send_message(note_on)
                    opacity +=2
                    print(opacity)
                    millumin.send_message("/millumin/layer/opacity/1", opacity)
                    # millumin.send_message("/millumin/layer/opacity/2", opacity)
                footX = 640 - f[0] 
                footY = 480 - f[1]
                processing.send_message("/foot", [footX, footY])
                
                if (stage == 5):    
                    angle = random.random()*2-1
                    shiftx = footX/640
                    shifty = footY/(480-cutY)

                    coge.send_message("/sharpen", sharpen)
                    coge.send_message("/angle", angle)
                    coge.send_message("/shiftx", shiftx)
                    coge.send_message("/shifty", shifty)
                   
                if (stage == 6):
                    opacity -= 1
                    millumin.send_message("/millumin/layer/opacity/1", opacity)
                    millumin.send_message("/millumin/layer/opacity/2", opacity)
                    # coge.send_message("/opacity", opacity/fadesteps)
                    op = int(opacity/100*127)
                    
                    if (op > 127):
                        op = 127
                    if (op < 0):
                        op = 0
                    control = [0xb0, 0x74, opacity]
                    midiout.send_message(control)


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
# time.sleep(startupdelay)
counter = 0
fadesteps = opacity  
starttime = time.time() ## time the cycle is first started.
feettime = starttime
countertime = starttime
processing.send_message("/stage", 0) ### black!!!
millumin.send_message("/millumin/layer/opacity/1", 0)
millumin.send_message("/millumin/layer/opacity/2", 100) 
while(1):

    if (len(lastfeet) == 0 and stage != 0):
        #check how long it has been zero
        zerotime = time.time() - feettime
        if (zerotime > shutdowntimeout):
            stage = 0 ## shut down the experience
            processing.send_message("/stage", 0) ### black!!!
            note_on = [0x90, 0, 100] # channel 1, middle C, velocity 112
            midiout.send_message(note_on)
    if (len(lastfeet) !=0):
        feettime = time.time() 
    
    if (stage == 0 and len(lastfeet) !=0):
        starttime = time.time()
        control = [0xb0, 0x74, 106]
        midiout.send_message(control)
        stage = 1
        note_on = [0x90, 1, 100] # channel 1, middle C, velocity 112
        midiout.send_message(note_on)
        # coge.send_message("/opacity", 0)
        millumin.send_message("/millumin/layer/opacity/1", 0)
        millumin.send_message("/millumin/layer/opacity/2", 100)            
        processing.send_message("/stage", 1) ### A_floorfiller
    
    if ( ((time.time() - starttime) > stage1time) and stage == 1 ) :
        stage = 2
        note_on = [0x90, 2, 100] # channel 1, middle C, velocity 112
        midiout.send_message(note_on)
        processing.send_message("/stage", 2)  ### B_FirstWave
    
    if ( ((time.time() - starttime) > stage2time) and stage == 2 ) :
        stage = 3
        processing.send_message("/stage", 3)  ### C_CircleWaves
    
    if ( ((time.time() - starttime) > stage3time) and stage == 3 ) :
        stage = 4
        note_on = [0x90, 3, 100] # channel 1, middle C, velocity 112
        midiout.send_message(note_on)
        processing.send_message("/stage", 4)  ### D_linewaves
    
    if ( ((time.time() - starttime) > stage4time) and stage == 4 ) :
        # coge.send_message("/opacity", 1)
        stage = 5
        processing.send_message("/stage", 5)  ### E_squarewaves

    if ( ((time.time() - starttime) > stage5time) and stage == 5 ) :
        # coge.send_message("/opacity", 1)
        opacity =100
        stage = 6
        millumin.send_message("/millumin/layer/opacity/1", 100)
        millumin.send_message("/millumin/layer/opacity/2", 100)
        processing.send_message("/stage", 6)  ### F_reset processing, focus on CoGe
    
    if (time.time() - countertime) > 1 :
        countertime = time.time()
        print("set counter so it's not going to fast")
        processFeet(testDepth())
        print(lastfeet)
    # print(feettime, starttime)
    



## Release resources
midiout.close_port()
del midiout
midiin.close_port()
del midiin
cv.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")
