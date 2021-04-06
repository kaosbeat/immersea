//import milchreis.imageprocessing.*;
//import milchreis.imageprocessing.utils.*;
import themidibus.*; //Import the library

MidiBus myBus; // The MidiBus


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
  cw = new CircleWaves(); 
  sw = new SquareWaves();
  lw = new LineWaves();

  MidiBus.list(); // List all available Midi devices on STDOUT. This will show each device's index and name.
  myBus = new MidiBus(this, 2, -1);
}

void draw() {
  clear();
  update();
  lw.run();
  //cw.run();
  //sw.run();

  if (counter % 50 == 0) {
    float r = random(10);
    float xpos = random(width);
    float ypos = random(height);
    float scale = random(0.3) + 0.2;
    int speed = int(random(10));
    if (r > 5) {

      int size = int(random(9));
      cw.addRipple(new PVector(xpos, ypos), size, speed, speed/3, scale);
    } else {

      int size = int(random(4));
      sw.addRipple(new PVector(xpos, ypos), size, speed, speed/3, scale);
    }
  }
  if (counter % 3 == 0) {
    //addWave(PVector pos, int size, int speed, float decay, PVector velocity )
    //println("adding wave");
    lw.addWave(new PVector(-70, -350), 10, 50, 0.5, new PVector(0, midi1/10));
  }
}

void update() {
  counter += 1;
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
