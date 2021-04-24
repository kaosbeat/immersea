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


  void startWave(PVector startpos, PVector endpos, int steps) {
    ///addallcircles
    int divx = 28;
    int divy = 18;
    for (int i = 0; i <= divx; i++) {
      for (int j = 0; j <= divy; j++) {
        int img = int(random(9));
        float scale = random(0.3, 0.5);
        blackcircles.add(new blackCircle(new PVector(startpos.x + i*width/divx, startpos.y + j*height/divy), new PVector(endpos.x + i*width/divx, endpos.y + j*height/divy), fillersimg[img], steps, i, scale));
      }
    }
  }

  void run() {
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

  void reset() {
    blackcircles = new ArrayList<blackCircle>();
  }
  
  void fadeall(){
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
    rot = random(3.14);
    acceleration = new PVector(0.05, 0);
    velocity = new PVector((endposition.x- position.x)/movesteps + speed * 0.03  , (endposition.y- position.y)); 
    noiseX = 0;
    noiseY = 0;
    //println("blackcircle added" + str(position.y));
  }

  void run() {
    update();
    display();
  }

  // Method to update position
  void update() {
    if (startposition.x - position.x < width/4 ) {
      //position.add(velocity);
      velocity.x -= 0.01;
    } else if (startposition.x - position.x < width) {
      
      //velocity.x += 0.03;
      velocity.x *= 0.9920;
    } 
    if (startposition.x - position.x > width + width/25) {
      velocity.x = 0;
    }
    position.add(velocity);
    noiseX += random(0.01, 0.05);
    noiseY += random(0.01, 0.05) ;
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
  void display() {

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
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }
}
