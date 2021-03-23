import netP5.*;
import oscP5.*;

OscP5 oscP5;

int m1pos[] = {0, 0};
int m2pos[] = {100, 0};
int m3pos[] = {100, 100};
int m4pos[] = {0, 100};
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



int p1pos[] = {50, 50};
int p2pos[] = {60, 60};
int p3pos[] = {70, 70};
int p4pos[] = {80, 80};
int cp1pos[] = {50, 50}; //remapped positions
int cp2pos[] = {60, 60};
int cp3pos[] = {70, 70};
int cp4pos[] = {80, 80};

void setup() {
  size(640, 480, P2D);
  oscP5 = new OscP5(this, 12000);
  rectMode(RADIUS);
}


void draw() {
  clear();
  background(0);
  testOverBox();
  remapFeet();
  drawPadding();
  fill(255, 0, 0);
  rect(p1pos[0], p1pos[1], 15, 15);
  rect(p2pos[0], p2pos[1], 15, 15);
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


void remapFeet(){
//m1pos[]


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
