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

  PImage circles[] = {c1, c2, c3,c4,c5,c6,c7,c8,c9,c10};
  CircleWaves() {
    circlewaves = new ArrayList<Circlewave>();
  }

  void addCircle(PVector pos, PImage img, int speed, float decay, int index, float scale) {
    circlewaves.add(new Circlewave(pos, img, speed, decay, index, scale));
  }

  void addRipple(PVector pos, int size, int speed, float decay, float scale ) {
    for (int i = 0; i <= size; i++) {
      addCircle(pos, circles[i], speed, decay, i, scale);
    }
  }

  void run() {
    for (int i = 0; i <= circlewaves.size()-1; i++) {
      Circlewave p = circlewaves.get(i);
      p.run();
      if (p.isDead()) {
        circlewaves.remove(i);
      }
    }
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
    acceleration = new PVector(0, 0.05);
    velocity = new PVector(random(-1, 1), random(-2, 0));
    position = l.copy();
    lifespan = 255;
    decay = 0.5 + decayspeed;
    prelife = speed*index;
    circleimg = img;
    circleScale = scale;
    rot = random(3.14);
  }

  void run() {
    update();
    display();
  }

  // Method to update position
  void update() {
    circleScale += 0.001;
    //velocity.add(acceleration);
    //position.add(velocity);
    prelife -= 1;
    if (prelife <= 0) {
      lifespan -= decay;
    }
  }

  // Method to display
  void display() {
    //stroke(255, lifespan);
    //fill(255, lifespan);
    //ellipse(position.x, position.y, 8, 8);
    if (prelife <= 0 ) {
      tint(255, lifespan);
      float xsize = circleScale*circleimg.width;
      float ysize = circleScale*circleimg.height;
      pushMatrix();
      translate(position.x, position.y);
      rotate(rot);
      image(circleimg, - xsize/2, - ysize/2, xsize, ysize);
      popMatrix();
    }
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
