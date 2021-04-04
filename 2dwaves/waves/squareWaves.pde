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
  PImage circles[] = {d1, d2, d3,d4,d5};
  SquareWaves() {
    squarewaves = new ArrayList<Squarewave>();
  }

  void addCircle(PVector pos, PImage img, int speed, float decay, int index, float scale) {
    squarewaves.add(new Squarewave(pos, img, speed, decay, index, scale));
  }

  void addRipple(PVector pos, int size, int speed, float decay, float scale ) {
    for (int i = 0; i <= size; i++) {
      addCircle(pos, circles[i], speed, decay, i, scale);
    }
  }

  void run() {
    for (int i = 0; i <= squarewaves.size()-1; i++) {
      Squarewave p = squarewaves.get(i);
      p.run();
      if (p.isDead()) {
        squarewaves.remove(i);
      }
    }
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
    acceleration = new PVector(0, 0.05);
    velocity = new PVector(random(-1, 1), random(-2, 0));
    position = l.copy();
    lifespan = 255;
    decay = 0.5 + decayspeed;
    prelife = speed*index;
    circleimg = img;
    circleScale = scale;
    rot = random(3.14);
    t = int(random(5)); 
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
        tint(255,lifespan);
      }
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
