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

  void addLine(PVector pos, PImage img, int speed, float decay, int index, PVector velocity) {
    linewaves.add(new Linewave(pos, img, speed, decay, index, velocity));
  }

  void addWave(PVector pos, int size, int speed, float decay, PVector velocity ) {
    for (int i = 0; i <= size; i++) {
      int r = int(random(lines.length));
      pos.y += i*4; 
      addLine(pos, lines[r], speed, decay, i, velocity);
    }
  }

  void run() {
    for (int i = 0; i <= linewaves.size()-1; i++) {
      Linewave p = linewaves.get(i);
      p.run();
      if (p.isDead()) {
        linewaves.remove(i);
      }
    }
  }
  
  void reset() {
    linewaves = new ArrayList<Linewave>();
  }
 void fadeAll() {
    for (int i = 0; i <= linewaves.size()-1; i++) {
      Linewave p = linewaves.get(i);
      p.opacity = ((p.opacity*100) - 0.4)/100;
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
    acceleration = new PVector(0.05, 0);
    //velocity = new PVector(random(-1, 1), random(-2, 0));
    velocity = v.copy();
    position = l.copy();
    lifespan = 255;
    decay = 0.7 + decayspeed;
    //prelife = speed*index;
    prelife = 0;
    lineimg = img;
    lineScale = 0.7;
    rot = random(3.14);
    t = int(random(5));
    opacity = 1;
  }

  void run() {
    update();
    display();
  }

  // Method to update position
  void update() {
    //circleScale += 0.001;
    
    float y = position.y;
    float x = position.x;
    y = y/height * 10;
    x = x/width * 50;
    acceleration.x = 0.6*(sin(abs(x))*random(1));
    acceleration.y = 0.01*(sin(abs(y))+0.01);
    velocity.add(acceleration);
    position.add(velocity);
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
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }
}
