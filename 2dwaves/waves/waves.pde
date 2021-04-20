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
// stage 3: more dynamic movement of the background
// stage 4: external waves
// stage 5: colourfull overlays wherever a foot is set

int currentstage;


CircleWaves cw;
SquareWaves sw;
LineWaves lw;
int midi1 = 64;
int midi2 = 64;
int counter;

void setup() {
  size(900, 900, P2D);
  background(0);
  counter = 0;
  currentstage = 0;
  ff = new FloorFillers();
  cw = new CircleWaves(); 
  sw = new SquareWaves();
  lw = new LineWaves();

  MidiBus.list(); // List all available Midi devices on STDOUT. This will show each device's index and name.
  myBus = new MidiBus(this, 2, -1);
  oscP5 = new OscP5(this, 12000);
  server = new SyphonServer(this, "Processing Syphon");
}





void draw() {
  clear();
  background(0);
  update();
  if (currentstage == 1) {
    ff.run();
  
  }
  if (currentstage == 2) {
    ff.reset();
  }
  
  //lw.run();
  cw.run();
  sw.run();

  //if (counter % 150 == 0) {
    //print("reset");
    
  //  float r = random(10);
  //  float xpos = random(width);
  //  float ypos = random(height);
  //  float scale = random(0.3) + 0.2;
  //  int speed = int(random(10));
  //  if (r > 5) {

  //    int size = int(random(9));
  //    cw.addRipple(new PVector(xpos, ypos), size, speed, speed/3, scale);
  //  } else {

  //    int size = int(random(4));
  //    sw.addRipple(new PVector(xpos, ypos), size, speed, speed/3, scale);
  //  }
  //}
  //if (counter % 3 == 0) {
  //  //addWave(PVector pos, int size, int speed, float decay, PVector velocity )
  //  //println("adding wave");
  //  lw.addWave(new PVector(-70, -350), 10, 50, 0.5, new PVector(0, midi1/10));
  //}
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
    float scale = random(0.3) + 0.2;
    int speed = int(random(10));
    int size = int(random(4))+2;
    //cw.addRipple(new PVector(x, y),size, speed, speed/3, scale);
    if (currentstage == 1) {
      float decay = 2;
      ff.addFiller(new PVector(x, y),size, speed, decay, scale*5);
    } else if (currentstage == 2) {
      println ("curretnstage = 2");
      cw.addRipple(new PVector(x, y), size, speed, speed/3, scale);
    } else if (currentstage == 3) {
      println ("curretnstage = 3");
      sw.addRipple(new PVector(x, y), size, speed, speed/3, scale);
    }
  }
  if (theOscMessage.checkAddrPattern("/stage")==true) {
    currentstage = theOscMessage.get(0).intValue();
  }
}
