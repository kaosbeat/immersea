import netP5.*;
import oscP5.*;

OscP5 oscP5;

int m1pos[] = {1, 1}; //TopLeft
int m2pos[] = {100, 1}; // TopRight
int m3pos[] = {100, 100}; //BottomRight
int m4pos[] = {1, 100}; //BottomLeft
int boxSize = 15;
boolean overBox1 = false;
boolean overBox2 = false;
boolean overBox3 = false;
boolean overBox4 = false;
boolean box1Locked = false;
boolean box2Locked = false;
boolean box3Locked = false;
boolean box4Locked = false;
int projectionpadding = 100;
int xOffset = 0; 
int yOffset = 0; 



int p1pos[] = {350, 350};
int p2pos[] = {60, 60};
int p3pos[] = {70, 70};
int p4pos[] = {80, 80};
float cp1pos[] = {50, 50}; //remapped positions
float cp2pos[] = {60, 60};
float cp3pos[] = {70, 70};
float cp4pos[] = {80, 80};

void setup() {
  size(640, 480, P2D);
  oscP5 = new OscP5(this, 12000);
  rectMode(RADIUS);
}


void draw() {
  clear();
  background(0);
  testOverBox();
  remapFeet(p1pos[0], p1pos[1]);
  drawPadding();
  fill(255, 0, 0);
  rect(p1pos[0], p1pos[1], 15, 15);
  fill(255, 255, 0);
  rect(cp1pos[0], cp1pos[1], 25, 25);
}
void drawPadding(){
  stroke(0,0,255);
  noFill();
  rect(width/2,height/2,width/2-projectionpadding, height/2-projectionpadding);
  stroke(0,0,0);
}

void testOverBox() {
  if (mouseX > m1pos[0]-boxSize && mouseX < m1pos[0]+boxSize && 
    mouseY > m1pos[1]-boxSize && mouseY < m1pos[1]+boxSize) {
    overBox1 = true;
    overBox2 = false;  
    overBox3 = false;  
    overBox4 = false;  
    if (!box1Locked ) { 
      stroke(255); 
      fill(153);
      rect(m1pos[0], m1pos[1], boxSize, boxSize);
      rect(m2pos[0], m2pos[1], boxSize, boxSize);
      rect(m3pos[0], m3pos[1], boxSize, boxSize);
      rect(m4pos[0], m4pos[1], boxSize, boxSize);
    }
  } else if (mouseX > m2pos[0]-boxSize && mouseX < m2pos[0]+boxSize && 
    mouseY > m2pos[1]-boxSize && mouseY < m2pos[1]+boxSize) {
    overBox1 = false;
    overBox2 = true;  
    overBox3 = false;  
    overBox4 = false;  
    if (!box2Locked ) { 
      stroke(255); 
      fill(153);
      rect(m1pos[0], m1pos[1], boxSize, boxSize);
      rect(m2pos[0], m2pos[1], boxSize, boxSize);
      rect(m3pos[0], m3pos[1], boxSize, boxSize);
      rect(m4pos[0], m4pos[1], boxSize, boxSize);
    }
  } else if (mouseX > m3pos[0]-boxSize && mouseX < m3pos[0]+boxSize && 
    mouseY > m3pos[1]-boxSize && mouseY < m3pos[1]+boxSize) {
    overBox1 = false;
    overBox2 = false;  
    overBox3 = true;  
    overBox4 = false;  
    if (!box3Locked ) { 
      stroke(255); 
      fill(153);
      rect(m1pos[0], m1pos[1], boxSize, boxSize);
      rect(m2pos[0], m2pos[1], boxSize, boxSize);
      rect(m3pos[0], m3pos[1], boxSize, boxSize);
      rect(m4pos[0], m4pos[1], boxSize, boxSize);
    }
  } else if (mouseX > m4pos[0]-boxSize && mouseX < m4pos[0]+boxSize && 
    mouseY > m4pos[1]-boxSize && mouseY < m4pos[1]+boxSize) {
    overBox1 = false;
    overBox2 = false;  
    overBox3 = false;  
    overBox4 = true;  
    if (!box4Locked ) { 
      stroke(255); 
      fill(153);
      rect(m1pos[0], m1pos[1], boxSize, boxSize);
      rect(m2pos[0], m2pos[1], boxSize, boxSize);
      rect(m3pos[0], m3pos[1], boxSize, boxSize);
      rect(m4pos[0], m4pos[1], boxSize, boxSize);
    }
  } else {
    stroke(153);
    fill(153);
    overBox1 = false;
    overBox2 = false;  
    overBox3 = false;  
    overBox4 = false;
    rect(m1pos[0], m1pos[1], boxSize, boxSize);
    rect(m2pos[0], m2pos[1], boxSize, boxSize);
    rect(m3pos[0], m3pos[1], boxSize, boxSize);
    rect(m4pos[0], m4pos[1], boxSize, boxSize);
  }
}


void mousePressed() {
  if (overBox1) { 
    box1Locked = true;
    box2Locked = false;
    box3Locked = false;
    box4Locked = false;
    fill(255, 255, 255);
    xOffset = mouseX-m1pos[0]; 
    yOffset = mouseY-m1pos[1];
  } else if (overBox2) { 
    box1Locked = false;
    box2Locked = true; 
    box3Locked = false;
    box4Locked = false;
    fill(255, 255, 255);
    xOffset = mouseX-m2pos[0]; 
    yOffset = mouseY-m2pos[1];
  } else if (overBox3) { 
    box1Locked = false;
    box2Locked = false; 
    box3Locked = true;
    box4Locked = false;
    fill(255, 255, 255);
    xOffset = mouseX-m3pos[0]; 
    yOffset = mouseY-m3pos[1];
  } else if (overBox4) { 
    box1Locked = false;
    box2Locked = false; 
    box3Locked = false;
    box4Locked = true;
    fill(255, 255, 255);
    xOffset = mouseX-m4pos[0]; 
    yOffset = mouseY-m4pos[1];
  } else {
    fill(255, 255, 255);
    box1Locked = false;
    box2Locked = false;
    box3Locked = false;
    box4Locked = false;
  }

}


void mouseDragged() {
  if (box1Locked) {
    m1pos[0] = mouseX-xOffset; 
    m1pos[1] = mouseY-yOffset;
  } else if (box2Locked) {
    m2pos[0] = mouseX-xOffset; 
    m2pos[1] = mouseY-yOffset;
  } else if (box3Locked) {
    m3pos[0] = mouseX-xOffset; 
    m3pos[1] = mouseY-yOffset;
  } else if (box4Locked) {
    m4pos[0] = mouseX-xOffset; 
    m4pos[1] = mouseY-yOffset;
  }

  rect(m1pos[0], m1pos[1], boxSize, boxSize);
  rect(m2pos[0], m2pos[1], boxSize, boxSize);
  rect(m3pos[0], m3pos[1], boxSize, boxSize);
  rect(m4pos[0], m4pos[1], boxSize, boxSize);
}

void mouseReleased() {
  box1Locked = false;
  box2Locked = false;
  box3Locked = false;
  box4Locked = false;
}


void remapFeet(int x, int y){
//m1pos[]
// calculate weights
float xmin = min(m1pos[0], m4pos[0]); ///min and max values used in calcs
float xmax = max(m2pos[0], m3pos[0]);
float ymin = min(m1pos[1], m2pos[1]);
float ymax = max(m4pos[1], m3pos[1]);

/////mapping vars
//if (m1pos[0] == 0) {m1pos[0] = 1;} ////dirty fix div by zero error!!
//if (m1pos[1] == 0) {m1pos[1] = 1;} 
//if (m2pos[0] == 0) {m2pos[0] = 1;} 
//if (m2pos[1] == 0) {m2pos[1] = 1;}
//if (m4pos[0]- m1pos[0] == 0) { m4pos[0] = m4pos[0] + 1;}
//if (m3pos[0]- m2pos[0] == 0) { m3pos[0] = m3pos[0] + 1;}
//if (m2pos[1]- m1pos[1] == 0) { m2pos[1] = m2pos[1] + 1;}
//if (m3pos[1]- m2pos[0] == 0) { m3pos[1] = m3pos[1] + 1;}

//float minx = xmin + (abs(y-m1pos[1]) / (0.01 + abs(m4pos[1]/(0.01 + m1pos[1]))) * abs(m4pos[0]-m1pos[0])) ;
//float maxx = xmax - (abs(y-m2pos[1]) / (0.01 + abs(m3pos[1]/(0.01 + m2pos[1]))) * abs(m3pos[0]-m2pos[0])) ;

//float miny = ymin + (abs(x-m1pos[0]) / (0.01 + abs(m2pos[0]/(0.01 + m1pos[0]))) * abs(m2pos[1]-m1pos[1])) ;
//float maxy = ymax - (abs(x-m2pos[0]) / (0.01 + abs(m3pos[0]/(0.01 + m2pos[0]))) * abs(m3pos[1]-m2pos[1])) ;

float minx = xmin + abs(y-m1pos[1]);


println(xmin,xmax,ymin,ymax);
println("calculated =", minx );
//println(minx,maxy,miny,maxy);


//cp1pos[0] = map(x, 0, width, minx, maxx);
//cp1pos[1] = map(y, 0, height, miny, maxy);

}



void oscEvent(OscMessage theOscMessage) {
  //print("### received an osc message.");
  //print(" addrpattern: "+theOscMessage.addrPattern());
  //println(" typetag: "+theOscMessage.typetag());
  //println("time" + millis()/1000 + "___" + theOscMessage.get(0).floatValue());
  if (theOscMessage.checkAddrPattern("/cnt0/cX")==true) {
    p1pos[0] = theOscMessage.get(0).intValue();
  }
  if (theOscMessage.checkAddrPattern("/cnt0/cY")==true) {
    p1pos[1] = theOscMessage.get(0).intValue();
  }
  if (theOscMessage.checkAddrPattern("/cnt1/cX")==true) {
    p2pos[0] = theOscMessage.get(0).intValue();
  }
  if (theOscMessage.checkAddrPattern("/cnt1/cY")==true) {
    p2pos[1] = theOscMessage.get(0).intValue();
  }
}
