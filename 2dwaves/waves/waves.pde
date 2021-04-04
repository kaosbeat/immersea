CircleWaves cw;
SquareWaves sw;
int counter;

void setup() {
  size(900, 900, P2D);
  background(0);
  counter = 0;
  cw = new CircleWaves(); 
  sw = new SquareWaves();
}

void draw() {
  clear();
  update();
  cw.run();
  sw.run();
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
}

void update() {
  counter += 1;
}
