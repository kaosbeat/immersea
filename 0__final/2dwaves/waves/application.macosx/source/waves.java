import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import themidibus.*; 
import netP5.*; 
import oscP5.*; 
import codeanticode.syphon.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class waves extends PApplet {

//import milchreis.imageprocessing.*;
//import milchreis.imageprocessing.utils.*;
 //Import the library



OscP5 oscP5;


MidiBus myBus; // The MidiBus


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

public void setup() {
  
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





public void draw() {
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
      lw.addWave(new PVector(-70, -250), 10, 50, 0.5f, new PVector(midi1/10, 0));
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

public void update() {
  counter += 1;
}

public void stage0() {
}



public void controllerChange(int channel, int number, int value) {
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

public void oscEvent(OscMessage theOscMessage) {
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
    float scale = random(0.2f) + 0.05f;
    int speed = PApplet.parseInt(random(10));
    int size = PApplet.parseInt(random(4))+2;
    //cw.addRipple(new PVector(x, y),size, speed, speed/3, scale);
    if (currentstage == 1) {
      float decay = 15;
      int img = PApplet.parseInt(random(9));
      ff.addFiller(new PVector(x, y), img, speed, decay, scale*5);
    } else if (currentstage == 2) {
      println ("curretnstage = 2");
    } else if (currentstage == 3) {
      int cwspeed = PApplet.parseInt(random(5));
      cw.addRipple(new PVector(x, y), size, cwspeed, cwspeed/3, scale);
      println ("curretnstage = 3");
    } else if (currentstage == 4) {
      
      println ("curretnstage = 4");
    } else if (currentstage == 5) {
      int swspeed = PApplet.parseInt(random(5));
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
// A class to describe a group of Floor Elements to fill the floor
// An ArrayList is used to manage the list

class FloorFillers {
  ArrayList<Filler> fillers;
  PVector origin;
  //PImage c1,c2,c3;
  PImage ff1 = loadImage("ff1.png");
  PImage ff2 = loadImage("ff2.png");
  PImage ff3 = loadImage("ff3.png");
  PImage ff4 = loadImage("ff4.png");
  PImage ff5 = loadImage("ff5.png");
  PImage ff6 = loadImage("ff6.png");
  PImage ff7 = loadImage("ff7.png");
  PImage ff8 = loadImage("ff8.png");
  PImage ff9 = loadImage("ff9.png");
  //PImage ff10 = loadImage("ff1.png");

  PImage fillersimg[] = {ff1, ff2, ff3,ff4,ff5,ff6,ff7,ff8,ff9};
  FloorFillers() {
    fillers = new ArrayList<Filler>();
  }

  public void addFiller(PVector pos, int img, int speed, float decay,  float scale) {
    fillers.add(new Filler(pos, fillersimg[img], speed, decay, scale));
  }

  //void addRipple(PVector pos, int size, int speed, float decay, float scale ) {
  //  for (int i = 0; i <= size; i++) {
  //    addFiller(pos, fillersimg[i], speed, decay, i, scale);
  //  }
  //}

  public void run() {
    for (int i = 0; i <= fillers.size()-1; i++) {
      Filler p = fillers.get(i);
      p.run();
      if (p.isDead()) {
        fillers.remove(i);
      }
    }
  }
  
  public void reset(){
    fillers = new ArrayList<Filler>();
  }
}


// A simple Particle class

class Filler {
  int number;
  PVector position;
  PVector velocity;
  PVector acceleration;
  float lifespan, decay;
  int prelife;
  PImage ffimg;
  float circleScale;
  float rot;
  float noiseX,noiseY;

  Filler(PVector l, PImage img, int speed, float decayspeed, float scale) {
    acceleration = new PVector(0, 0.05f);
    velocity = new PVector(random(-1, 1), random(-2, 0));
    noiseX = 0;
    position = l.copy();
    lifespan = 1;
    decay = decayspeed;
    ffimg = img;
    circleScale = scale *0.6f;
    rot = random(3.14f);
  }

  public void run() {
    update();
    display();
  }

  // Method to update position
  public void update() {
    noiseX += 0.01f;
    noiseY += 0.02f;
    acceleration.x = sin(noiseX)*10;
    acceleration.y = sin(noiseY)*10;
    if (lifespan < 255){
      lifespan += decay;
    }
    //circleScale += 0.001;
    //velocity.add(acceleration);
    //position.add(velocity);
    //prelife -= 1;
    //if (prelife <= 0) {
    //  lifespan -= decay;
    //}
  }

  // Method to display
  public void display() {
      tint(255, lifespan);
      float xsize = circleScale*ffimg.width;
      float ysize = circleScale*ffimg.height;
      pushMatrix();
      translate(position.x + acceleration.x  , position.y + acceleration.y);
      rotate(rot);
      image(ffimg, - xsize/2, - ysize/2, xsize, ysize);
      popMatrix();
  }

  // Is the particle still useful?
  public boolean isDead() {
    if (lifespan < 0.0f) {
      return true;
    } else {
      return false;
    }
  }
}
// Wave filling the whole screen from left to right, and then slowly settling in 
// IMPORTANT wave goes from right to left! otherwise math does not compute

class FirstWave {
  ArrayList<blackCircle> blackcircles;
  PVector origin;
  //PImage c1,c2,c3;
  PImage ff1 = loadImage("ff1.png");
  PImage ff2 = loadImage("ff2.png");
  PImage ff3 = loadImage("ff3.png");
  PImage ff4 = loadImage("ff4.png");
  PImage ff5 = loadImage("ff5.png");
  PImage ff6 = loadImage("ff6.png");
  PImage ff7 = loadImage("ff7.png");
  PImage ff8 = loadImage("ff8.png");
  PImage ff9 = loadImage("ff9.png");

  PImage fillersimg[] = {ff1, ff2, ff3, ff4, ff5, ff6, ff7, ff8, ff9};
  FirstWave() {
    blackcircles = new ArrayList<blackCircle>();
  }


  public void startWave(PVector startpos, PVector endpos, int steps) {
    ///addallcircles
    int divx = 28;
    int divy = 18;
    for (int i = 0; i <= divx; i++) {
      for (int j = 0; j <= divy; j++) {
        int img = PApplet.parseInt(random(9));
        float scale = random(0.3f, 0.5f);
        blackcircles.add(new blackCircle(new PVector(startpos.x + i*width/divx, startpos.y + j*height/divy), new PVector(endpos.x + i*width/divx, endpos.y + j*height/divy), fillersimg[img], steps, i, scale));
      }
    }
  }

  public void run() {
    for (int i = 0; i <= blackcircles.size()-1; i++) {
      
       
      blackCircle p = blackcircles.get(i);
        //if (i == 0){
        //  //println(p.startposition.x - p.position.x);
        //}
      p.run();
      if (p.isDead()) {
        blackcircles.remove(i);
      }
    }
  }

  public void reset() {
    blackcircles = new ArrayList<blackCircle>();
  }
  
  public void fadeall(){
    for (int i = 0; i <= blackcircles.size()-1; i++) {
      blackCircle p = blackcircles.get(i);
      p.opacity -= 1;
    }
  }
  
}


// A simple Particle class

class blackCircle {
  int number, opacity;
  PVector position;
  PVector startposition, endposition;
  PVector velocity;
  PVector acceleration;
  float lifespan, decay;
  int movesteps, speed;
  PImage ffimg;
  float circleScale;
  float rot;
  float noiseX, noiseY;

  blackCircle(PVector l, PVector endpos, PImage img, int steps, int speed, float scale) {
    opacity = 255;
    startposition = l.copy();
    position = l.copy();
    endposition = endpos.copy(); 
    movesteps = steps;
    ffimg = img;
    circleScale = scale;
    rot = random(3.14f);
    acceleration = new PVector(0.05f, 0);
    velocity = new PVector((endposition.x- position.x)/movesteps + speed * 0.03f  , (endposition.y- position.y)); 
    noiseX = 0;
    noiseY = 0;
    //println("blackcircle added" + str(position.y));
  }

  public void run() {
    update();
    display();
  }

  // Method to update position
  public void update() {
    if (startposition.x - position.x < width/4 ) {
      //position.add(velocity);
      velocity.x -= 0.01f;
    } else if (startposition.x - position.x < width) {
      
      //velocity.x += 0.03;
      velocity.x *= 0.9920f;
    } 
    if (startposition.x - position.x > width + width/25) {
      velocity.x = 0;
    }
    position.add(velocity);
    noiseX += random(0.01f, 0.05f);
    noiseY += random(0.01f, 0.05f) ;
    acceleration.x = sin(noiseX)*10;
    acceleration.y = sin(noiseY)*10;
    //if (lifespan < 255){
    //  lifespan += decay;
    //}
    //circleScale += 0.001;
    //velocity.add(acceleration);
    //position.add(velocity);
    //prelife -= 1;
    //if (prelife <= 0) {
    //  lifespan -= decay;
    //}
  }

  // Method to display
  public void display() {

    tint(255,opacity);
    float xsize = circleScale*ffimg.width;
    float ysize = circleScale*ffimg.height;
    pushMatrix();
    translate(position.x + acceleration.x, position.y + acceleration.y);
    rotate(rot);
    image(ffimg, - xsize/2, - ysize/2, xsize, ysize);
    popMatrix();
  }

  // Is the particle still useful?
  public boolean isDead() {
    if (lifespan < 0.0f) {
      return true;
    } else {
      return false;
    }
  }
}
// A class to describe a group of Particles
// An ArrayList is used to manage the list of Particles 

class CircleWaves {
  ArrayList<Circlewave> circlewaves;
  PVector origin;
  //PImage c1,c2,c3;
  PImage c1 = loadImage("c1.png");
  PImage c2 = loadImage("c2.png");
  PImage c3 = loadImage("c3.png");
  PImage c4 = loadImage("c4.png");
  PImage c5 = loadImage("c5.png");
  PImage c6 = loadImage("c6.png");
  PImage c7 = loadImage("c7.png");
  PImage c8 = loadImage("c8.png");
  PImage c9 = loadImage("c9.png");
  PImage c10 = loadImage("c10.png");

  PImage circles[] = {c1, c2, c3, c4, c5, c6, c7, c8, c9, c10};
  CircleWaves() {
    circlewaves = new ArrayList<Circlewave>();
  }

  public void addCircle(PVector pos, PImage img, int speed, float decay, int index, float scale) {
    circlewaves.add(new Circlewave(pos, img, speed, decay, index, scale));
  }

  public void addRipple(PVector pos, int size, int speed, float decay, float scale ) {
    for (int i = 0; i <= size; i++) {
      addCircle(pos, circles[i], speed, decay, i, scale);
    }
  }

  public void run() {
    for (int i = 0; i <= circlewaves.size()-1; i++) {
      Circlewave p = circlewaves.get(i);
      p.run();
      if (p.isDead()) {
        circlewaves.remove(i);
      }
    }
  }

  public void reset() {
    circlewaves = new ArrayList<Circlewave>();
  }
}


// A simple Particle class

class Circlewave {
  int number;
  PVector position;
  PVector velocity;
  PVector acceleration;
  float lifespan, decay;
  int prelife;
  PImage circleimg;
  float circleScale;
  float rot;

  Circlewave(PVector l, PImage img, int speed, float decayspeed, int index, float scale) {
    acceleration = new PVector(0, 0.05f);
    velocity = new PVector(random(-1, 1), random(-2, 0));
    position = l.copy();
    lifespan = 255;
    decay = 0.5f + decayspeed;
    prelife = speed*index;
    circleimg = img;
    circleScale = scale;
    rot = random(3.14f);
  }

  public void run() {
    update();
    display();
  }

  // Method to update position
  public void update() {
    circleScale += 0.001f;
    //velocity.add(acceleration);
    //position.add(velocity);
    prelife -= 1;
    if (prelife <= 0) {
      lifespan -= decay;
    }
  }

  // Method to display
  public void display() {
    //stroke(255, lifespan);
    //fill(255, lifespan);
    //ellipse(position.x, position.y, 8, 8);
    if (prelife <= 0 ) {

      float xsize = circleScale*circleimg.width;
      float ysize = circleScale*circleimg.height;
      pushMatrix();
      tint(255, lifespan);
      translate(position.x, position.y);
      rotate(rot);
      image(circleimg, - xsize/2, - ysize/2, xsize, ysize);
      popMatrix();
    }
  }

  // Is the particle still useful?
  public boolean isDead() {
    if (lifespan < 0.0f) {
      return true;
    } else {
      return false;
    }
  }
}
// A class to describe a group of Particles
// An ArrayList is used to manage the list of Particles 

class LineWaves {
  ArrayList<Linewave> linewaves;
  PVector origin;
  //PImage c1,c2,c3;
  PImage l1 = loadImage("l1.png");
  PImage l2 = loadImage("l2.png");
  PImage l3 = loadImage("l3.png");
  PImage l4 = loadImage("l4.png");
  PImage l5 = loadImage("l5.png");
  PImage lines[] = {l1, l2, l3, l4, l5};
  LineWaves() {
    linewaves = new ArrayList<Linewave>();
  }

  public void addLine(PVector pos, PImage img, int speed, float decay, int index, PVector velocity) {
    linewaves.add(new Linewave(pos, img, speed, decay, index, velocity));
  }

  public void addWave(PVector pos, int size, int speed, float decay, PVector velocity ) {
    for (int i = 0; i <= size; i++) {
      int r = PApplet.parseInt(random(lines.length));
      pos.y += i*4; 
      addLine(pos, lines[r], speed, decay, i, velocity);
    }
  }

  public void run() {
    for (int i = 0; i <= linewaves.size()-1; i++) {
      Linewave p = linewaves.get(i);
      p.run();
      if (p.isDead()) {
        linewaves.remove(i);
      }
    }
  }
  
  public void reset() {
    linewaves = new ArrayList<Linewave>();
  }
 public void fadeAll() {
    for (int i = 0; i <= linewaves.size()-1; i++) {
      Linewave p = linewaves.get(i);
      p.opacity = ((p.opacity*100) - 0.4f)/100;
    }
  }
}



// A simple Particle class

class Linewave {
  int number;
  PVector position;
  PVector velocity;
  PVector acceleration;
  float lifespan, decay;
  int prelife;
  PImage lineimg;
  float lineScale;
  float rot;
  int t;
  int index;
  float opacity;
  
  Linewave(PVector l, PImage img, int speed, float decayspeed, int index, PVector v) {
    acceleration = new PVector(0.05f, 0);
    //velocity = new PVector(random(-1, 1), random(-2, 0));
    velocity = v.copy();
    position = l.copy();
    lifespan = 255;
    decay = 0.7f + decayspeed;
    //prelife = speed*index;
    prelife = 0;
    lineimg = img;
    lineScale = 0.7f;
    rot = random(3.14f);
    t = PApplet.parseInt(random(5));
    opacity = 1;
  }

  public void run() {
    update();
    display();
  }

  // Method to update position
  public void update() {
    //circleScale += 0.001;
    
    float y = position.y;
    float x = position.x;
    y = y/height * 10;
    x = x/width * 50;
    acceleration.x = 0.6f*(sin(abs(x))*random(1));
    acceleration.y = 0.01f*(sin(abs(y))+0.01f);
    velocity.add(acceleration);
    position.add(velocity);
    prelife -= 1;
    if (prelife <= 0) {
      lifespan -= decay;
    }
  }


  // Method to display
  public void display() {
    //stroke(255, lifespan);
    //fill(255, lifespan);
    //ellipse(position.x, position.y, 8, 8);
    if (prelife <= 0 ) {
      tint(255, lifespan*opacity);
      pushMatrix();
      translate(position.x, position.y);
      //rotate(rot);
      //PImage processedImage = Glitch.apply(circleimg, 1, 15);
      float xsize = lineScale*lineimg.width;
      float ysize = lineScale*lineimg.height;
      image(lineimg, 0, 0, xsize, ysize);
      popMatrix();
    }
  }

  // Is the particle still useful?
  public boolean isDead() {
    if (lifespan < 0.0f) {
      return true;
    } else {
      return false;
    }
  }
}
// A class to describe a group of Particles
// An ArrayList is used to manage the list of Particles 

class SquareWaves {
  ArrayList<Squarewave> squarewaves;
  PVector origin;
  //PImage c1,c2,c3;
  PImage d1 = loadImage("d1.png");
  PImage d2 = loadImage("d2.png");
  PImage d3 = loadImage("d3.png");
  PImage d4 = loadImage("d4.png");
  PImage d5 = loadImage("d5.png");
  PImage circles[] = {d1, d2, d3, d4, d5};
  SquareWaves() {
    squarewaves = new ArrayList<Squarewave>();
  }

  public void addCircle(PVector pos, PImage img, int speed, float decay, int index, float scale) {
    squarewaves.add(new Squarewave(pos, img, speed, decay, index, scale));
  }

  public void addRipple(PVector pos, int size, int speed, float decay, float scale ) {
    for (int i = 0; i <= size; i++) {
      addCircle(pos, circles[i], speed, decay, i, scale);
    }
  }

  public void run() {
    for (int i = 0; i <= squarewaves.size()-1; i++) {
      Squarewave p = squarewaves.get(i);
      p.run();
      if (p.isDead()) {
        squarewaves.remove(i);
      }
    }
  }

  public void reset() {
    squarewaves = new ArrayList<Squarewave>();
  }
}


// A simple Particle class

class Squarewave {
  int number;
  PVector position;
  PVector velocity;
  PVector acceleration;
  float lifespan, decay;
  int prelife;
  PImage circleimg;
  float circleScale;
  float rot;
  int t;

  Squarewave(PVector l, PImage img, int speed, float decayspeed, int index, float scale) {
    acceleration = new PVector(0, 0.05f);
    velocity = new PVector(random(-1, 1), random(-2, 0));
    position = l.copy();
    lifespan = 255;
    decay = 0.5f + decayspeed;
    prelife = speed*index;
    circleimg = img;
    circleScale = scale;
    rot = random(3.14f);
    t = PApplet.parseInt(random(5));
  }

  public void run() {
    update();
    display();
  }

  // Method to update position
  public void update() {
    circleScale += 0.001f;
    //velocity.add(acceleration);
    //position.add(velocity);
    prelife -= 1;
    if (prelife <= 0) {
      lifespan -= decay;
    }
  }

  // Method to display
  public void display() {
    //stroke(255, lifespan);
    //fill(255, lifespan);
    //ellipse(position.x, position.y, 8, 8);
    if (prelife <= 0 ) {
      //tint(lifespan, lifespan);
      if (t == 0) {
        tint(0, 153, 204, lifespan);
      } else if (t == 1) {
        tint(255, 153, 24, lifespan);
      } else if (t == 2) {
        tint(255, lifespan, 24, lifespan);
      } else if (t == 3) {
        tint(lifespan, 153, lifespan, lifespan);
      } else {
        tint(255, lifespan);
      }
      float xsize = circleScale*circleimg.width;
      float ysize = circleScale*circleimg.height;
      pushMatrix();
      translate(position.x, position.y);
      rotate(rot);
      //PImage processedImage = Glitch.apply(circleimg, 1, 15);
      image(circleimg, - xsize/2, - ysize/2, xsize, ysize);
      popMatrix();
    }
  }

  // Is the particle still useful?
  public boolean isDead() {
    if (lifespan < 0.0f) {
      return true;
    } else {
      return false;
    }
  }
}
  public void settings() {  size(1920, 1080, P2D); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "waves" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
