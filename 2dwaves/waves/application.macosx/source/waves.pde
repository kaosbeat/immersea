//import milchreis.imageprocessing.*;
//import milchreis.imageprocessing.utils.*;
import themidibus.*; //Import the library
import netP5.*;
import oscP5.*;

OscP5 oscP5;


MidiBus myBus; // The MidiBus
import codeanticode.syphon.*;

SyphonServer server;


// stages
// stage 1: empty space, static circles waves appear wherever footsteps are set
FloorFillers ff;
// stage 2: transition to fully filled
FirstWave fw;
// stage 3: more dynamic movement of the background
CircleWaves cw;
// stage 4: sencond wave
LineWaves lw;
// stage 5: colourfull overlays wherever a foot is set
SquareWaves sw;

int currentstage;
int midi1 = 64;
int midi2 = 64;
int counter;
int lwcounter;

void setup() {
  size(1920, 1080, P2D);
  background(0);
  counter = 0;
  currentstage = 0;
  ff = new FloorFillers();
  fw = new FirstWave();
  cw = new CircleWaves(); 
  sw = new SquareWaves();
  lw = new LineWaves();


  MidiBus.list(); // List all available Midi devices on STDOUT. This will show each device's index and name.
  myBus = new MidiBus(this, 2, -1);
  oscP5 = new OscP5(this, 12000);
  server = new SyphonServer(this, "immersea P5");
}





void draw() {
  clear();
  //background(255);
  update();
  if (currentstage == 1) {
    ff.run();
  }
  if (currentstage == 2) {
    ff.run();
    fw.run();
  } 
  if (currentstage == 3) {
    fw.run();
    cw.run();
  }
  if (currentstage  == 4) {
    fw.fadeall();
    if (counter % 8 == 0 && lwcounter < 125) {
      //lw.addWave(new PVector(-70, -350), 10, 50, 0.5, new PVector(0, midi1/10));
      lw.addWave(new PVector(-70, -250), 10, 50, 0.5, new PVector(midi1/10, 0));
      lwcounter++;
    }
    fw.run();
    lw.run();
    cw.run();
  }
  if (currentstage  == 5) {
    lw.fadeAll();
    lw.run();
    sw.run();
  }
  if (currentstage  == 6) {
    
    sw.run();
  }
  server.sendScreen();
}

void update() {
  counter += 1;
}

void stage0() {
}



void controllerChange(int channel, int number, int value) {
  // Receive a controllerChange
  println();
  println("Controller Change:");
  println("--------");
  println("Channel:"+channel);
  println("Number:"+number);
  println("Value:"+value);
  if (number == 2) {
    midi1 = value;
  }
  if (number == 3) {
    midi2 = value;
  }
}

void oscEvent(OscMessage theOscMessage) {
  //print("### received an osc message.");
  //print(" addrpattern: "+theOscMessage.addrPattern());
  //println(" typetag: "+theOscMessage.typetag());
  //println("time" + millis()/1000 + "___" + theOscMessage.get(0).floatValue());
  if (theOscMessage.checkAddrPattern("/foot")==true) {
    float x = theOscMessage.get(0).intValue();
    float y = theOscMessage.get(1).intValue();
    x = map(x, 0, 640, 0, width) ;
    y = map(y, 0, 480, 0, height); 
    //println(x,y);
    float scale = random(0.2) + 0.05;
    int speed = int(random(10));
    int size = int(random(4))+2;
    //cw.addRipple(new PVector(x, y),size, speed, speed/3, scale);
    if (currentstage == 1) {
      float decay = 15;
      int img = int(random(9));
      ff.addFiller(new PVector(x, y), img, speed, decay, scale*5);
    } else if (currentstage == 2) {
      println ("curretnstage = 2");
    } else if (currentstage == 3) {
      int cwspeed = int(random(5));
      cw.addRipple(new PVector(x, y), size, cwspeed, cwspeed/3, scale);
      println ("curretnstage = 3");
    } else if (currentstage == 4) {
      
      println ("curretnstage = 4");
    } else if (currentstage == 5) {
      int swspeed = int(random(5));
      sw.addRipple(new PVector(x, y), size, swspeed, swspeed/3, scale);
      println ("curretnstage = 5");
    }
  }
  if (theOscMessage.checkAddrPattern("/stage")==true) {
    currentstage = theOscMessage.get(0).intValue();
    if (currentstage == 0) {
      ff.reset();
      fw.reset();
      lw.reset();
      cw.reset();
      sw.reset();
    }
    if (currentstage == 1) {
      //fw.reset();
      //lw.reset();
    }
    if (currentstage == 2) {
      //lw.reset();
      fw.startWave(new PVector(width, 0), new PVector(0, 0), 150);
    }
    if (currentstage == 3) {
      ff.reset();
      //lw.reset();
    } 
    if (currentstage == 4) {
      //fw.reset();
      lwcounter = 0;
    }
    if (currentstage == 5) {
      fw.reset();
    }
  }
}
