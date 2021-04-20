// A class to describe a group of Floor Elements to fill the floor
// An ArrayList is used to manage the list

class FloorFillers {
  ArrayList<Filler> fillers;
  PVector origin;
  //PImage c1,c2,c3;
  PImage ff1 = loadImage("ff1.png");
  PImage ff2 = loadImage("ff2.png");
  PImage ff3 = loadImage("ff3.png");
  PImage ff4 = loadImage("ff3.png");
  PImage ff5 = loadImage("ff2.png");
  PImage ff6 = loadImage("ff1.png");
  PImage ff7 = loadImage("ff2.png");
  PImage ff8 = loadImage("ff3.png");
  PImage ff9 = loadImage("ff1.png");
  PImage ff10 = loadImage("ff1.png");

  PImage fillersimg[] = {ff1, ff2, ff3,ff4,ff5,ff6,ff7,ff8,ff9,ff10};
  FloorFillers() {
    fillers = new ArrayList<Filler>();
  }

  void addFiller(PVector pos, int img, int speed, float decay,  float scale) {
    fillers.add(new Filler(pos, fillersimg[img], speed, decay, scale));
  }

  //void addRipple(PVector pos, int size, int speed, float decay, float scale ) {
  //  for (int i = 0; i <= size; i++) {
  //    addFiller(pos, fillersimg[i], speed, decay, i, scale);
  //  }
  //}

  void run() {
    for (int i = 0; i <= fillers.size()-1; i++) {
      Filler p = fillers.get(i);
      p.run();
      if (p.isDead()) {
        fillers.remove(i);
      }
    }
  }
  
  void reset(){
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
    acceleration = new PVector(0, 0.05);
    velocity = new PVector(random(-1, 1), random(-2, 0));
    noiseX = 0;
    position = l.copy();
    lifespan = 1;
    decay = decayspeed;
    ffimg = img;
    circleScale = scale;
    rot = random(3.14);
  }

  void run() {
    update();
    display();
  }

  // Method to update position
  void update() {
    noiseX += 0.01;
    noiseY += 0.02;
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
  void display() {
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
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }
}
