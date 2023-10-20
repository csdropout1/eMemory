public class HW1 {

  public static void main(String[] args) {
    Turtle kate = new Turtle();
  // Problem Check
  //  polyspiral(kate, 3, 20, 5);
  //  polywheel(kate, 5, 40);
  //  multistar(kate, 7, 100);
  //  pyramid(kate, 20, 5);
  //  houseline(kate, 4);
  // kate.penup();
  // kate.backward(450);
  // kate.pendown();
  // medivaltown(kate);
  }
  
//Problem 2
public static void medivaltown(Turtle t) {
  mountain(t);
  t.penup();
  t.forward(180);
  t.left(90);
  t.forward(40);
  t.right(90);
  t.pendown();
  mountain(t);
  t.penup();
  t.forward(210);
  t.right(90);
  t.forward(20);
  t.left(90);
  t.pendown();
  mountain(t);
  t.penup();
  t.backward(330);
  t.left(90);
  t.backward(50);
  t.right(90);
  t.pendown();
  pillar(t);
  t.penup();
  t.forward(250);
  t.pendown();
  pillar(t);
  t.penup();
  t.backward(180);
  t.right(90);
  t.forward(85);
  t.left(90);
  t.pendown();
  entirebrick(t);
  t.penup();
  t.forward(80);
  t.right(90);
  t.forward(30);
  t.left(90);
  t.pendown();
  arcs(t);
  t.penup();
  t.forward(40);
  t.pendown();
  entirebrick(t);
  t.penup();
  t.forward(150);
  t.right(90);
  t.forward(5);
  t.left(90);
  t.pendown();
  arcs3(t);
  t.penup();
  t.backward(50);
  t.right(90);
  t.forward(70);
  t.left(90);
  t.pendown();
  arrows4(t);
  t.penup();
  t.backward(170);
  t.right(90);
  t.forward(40);
  t.left(90);
  t.pendown();
  arrows4(t);
  t.penup();
  t.backward(70);
  t.left(90);
  t.forward(330);
  t.right(90);
  t.pendown();
  stars(t);
  t.penup();
  t.backward(80);
  t.right(90);
  t.forward(50);
  t.left(90);
  t.pendown();
  stars(t);
  t.penup();
  t.backward(60);
  t.left(90);
  t.forward(60);
  t.right(90);
  t.pendown();
  stars(t);
  t.penup();
  t.backward(130);
  t.right(90);
  t.forward(50);
  t.left(90);
  t.pendown();
  stars(t);
  t.penup();
  t.backward(40);
  t.left(90);
  t.forward(70);
  t.right(90);
  t.pendown();
  stars(t);
  t.penup();
  t.backward(80);
  t.right(90);
  t.forward(30);
  t.left(90);
  t.pendown();
  stars(t);
  t.penup();
  t.backward(80);
  t.pendown();
  stars(t);
  t.penup();
  t.forward(40);
  t.right(90);
  t.forward(40);
  t.left(90);
  t.pendown();
  stars(t);

}
//Utilizing a for loop to draw all three arcs together to save time.
public static void arcs3(Turtle t) {
  for (int i=0; i<3;i++){
    arcs(t);
    t.penup();
    t.forward(50);
    t.right(90);
    t.forward(10);
    t.left(90);
    t.pendown();
  }
}

//Creating the single arc.
public static void arcs(Turtle t) {
  t.left(90);
  t.forward(25);
  halfcircle(t, 2.06, 60);
  t.forward(30);
  t.right(90);
  t.forward(10);
  t.penup();
  t.forward(30);
  t.pendown();
  t.backward(10);
  t.right(90);
  t.forward(30);
  halfcircle(t, 1.047, 60);
  t.forward(30);
  t.penup();
  t.left(90);
  t.backward(30);
  t.left(90);
  t.forward(30);
  t.right(90);
  t.pendown();

}
//Since a half circle is half a circle, we can multiply 0.5 to a normal
//makeshift circle to create the arc for our arcs.
public static void halfcircle(Turtle t, double length, int numSides) {
  for (int i = 0; i < numSides*0.5; i++) {
    t.forward(length);
    t.right(360.0/numSides);
      }
}

//Using a forloop to repeat the two layers to simplify the process.
//Note, in retrospect, we could have easily created a function for each
//alternating pattern and then combined them.
public static void entirebrick(Turtle t) {
  for (int i =0; i<3; i++){
    brickrow(t);
  }
  bricks(t, 8);
  t.left(90);
  t.forward(30);
  t.right(90);
}
//creating a function for the first two layers since those are the layers that
//repeat.
public static void brickrow(Turtle t) {
  bricks(t, 8);
  t.right(90);
  t.forward(5);
  t.left(90);
  smolsquare(t);
  t.forward(5);
  bricks(t, 7);
  t.forward(70);
  smolsquare(t);
  t.backward(75);
  t.right(90);
  t.forward(5);
  t.left(90);
}
//Square for the brickwall.
//Doing the brickwall in parts, so it is easier to keep track of where
//the turtle is.
public static void smolsquare(Turtle t) {
  for (int i=0; i<4; i++){
    t.forward(5);
    t.right(90);
  }
}

//The rectangles for the brick wall.
public static void bricks(Turtle t, int n) {
  for (int i=0; i < n; i++){
    for (int j =0; j<2; j++){
      t.forward(10);
      t.right(90);
      t.forward(5);
      t.right(90);
    }
    t.forward(10);
  }
  t.backward(n*10);
}

//Was not sure how to improve the efficiency of creating this part.
//Drew the frame with regular turtle, used forloops for the squares.
public static void pillar(Turtle t) {
  for (int i = 0; i < 4; i++) {
    t.left(90);
    t.forward(10);
    t.right(90);
    t.forward(10);
    t.right(90);
    t.forward(10);
    t.left(90);
    t.forward(10);
    }
    t.left(90);
    t.forward(10);
    t.right(90);
    t.forward(10);
    t.right(90);
    t.forward(20);

    t.right(63.43);
    t.forward(22.36);
    t.left(63.43);
    t.forward(100);
    t.right(90);
    t.forward(50);
    t.right(90);
    t.forward(100);
    t.left(63.42);
    t.forward(22.36);
    t.right(63.43);
    t.forward(10);
    t.right(90);

    t.penup();
    t.forward(30);
    t.right(90);
    t.forward(10);
    t.left(90);
    t.pendown();
    pillarsquares(t);
    t.penup();
    t.forward(20);
    t.left(90);
    t.forward(60);
    t.right(90);
    t.pendown();
    pillarsquares(t);
    t.penup();
    t.backward(50);
    t.left(90);
    t.forward(70);
    t.right(90);
    t.pendown();
}
//Decided to draw the squares going down vertically so the function only
//needed to be called twice instead of three times in the future.
public static void pillarsquares(Turtle t) {
  for (int i =0; i < 3; i++){
    t.penup();
    t.right(90);
    t.forward(20);
    t.left(90);
    t.pendown();
    for (int j =0; j < 4; j++) {
      t.forward(10);
      t.right(90);
    }
  }
}

//Loop for a horizontal row of arrows.
public static void arrows4(Turtle t) {
  for (int i = 0; i<4; i++){
    arrows(t);
    t.penup();
    t.forward(30);
    t.pendown();
  }
}

//Individual arrows.
public static void arrows(Turtle t) {
    t.penup();
    t.forward(10);
    t.pendown();
    t.left(90);
    t.forward(40);
  for (int i = 0; i < 5; i++) {
    t.left(135);
    t.forward(14.142);
    t.backward(14.142);
    t.left(90);
    t.forward(14.142);
    t.backward(14.142);
    t.right(45);
    t.forward(5);
    t.right(180);
    }
    t.backward(15);
    t.right(90);
    t.penup();
    t.backward(10);
    t.pendown();
}

//Individual mountains
public static void mountain(Turtle t) {
    t.left(26.565);
    t.forward(178.88);
    t.right(90);
    t.forward(134.16);
    t.backward(134.16);
    t.left(90);
    t.backward(178.88);
    t.right(26.565);
}

//Each individual stars.
public static void stars(Turtle t) {
  for (int i = 0; i < 8; i++) {
    t.forward(10);
    t.backward(10);
    t.right(360.0/8);
    }
}

//Problem 3
  public static void polyspiral(Turtle t, int n, double base, int rounds) {
    // To orientate the Turtle.
      t.left(360.0/n);
    for (int i = 0; i < rounds; i++) {
      t.forward(i*base);
      t.right(360.0/n);
      }
  }


//Problem 4
public static void polywheel(Turtle t, int numSides, double length) {
    t.left(180);
  for (int i = 0; i < numSides; i++) {
    polygon(t, numSides, length);
    t.forward(length);
    t.left(360.0/numSides);
      }
  }

public static void polygon(Turtle t, int numSides, double length) {
  for (int i = 0; i < numSides; i++) {
    t.forward(length);
    t.right(360.0/numSides);
      }
  }

//Problem 5
public static void multistar(Turtle t, int n, double length) {
  for (int i = 0; i < n; i++) {
    ray(t, length);
    t.right(360.0/n);
      }
  }

public static void ray(Turtle t, double length) {
    t.forward(length);
  for (int i = 0; i < 10; i++) {
    t.forward(0.25*length);
    t.backward(0.25*length);
    t.right(36);
      }
    t.backward(length);
  }
//Problem 6
public static void pyramid(Turtle t, double base, int levels) {
  for (int i = 0; i < levels; i++) {
    squarerows(t, base, levels-i);
    t.left(90);
    t.forward(base);
    t.left(90);
    t.forward((levels-2*i) *base +3*base);
    t.right(180);
      }
  }

public static void squarerows(Turtle t, double base, int levels) {
  for (int i = 0; i < 2*levels-1; i++) {
    square(t, base);
    t.forward(base);
      }
    }

public static void square(Turtle t, double base) {
  for (int i = 0; i < 4; i++) {
    t.forward(base);
    t.left(90);
      }
    }

//Problem 7
public static void houseline(Turtle t, int numHouses) {
    t.penup();
    t.backward(400);
    t.pendown();
    house(t, 2);
  for (int i = 0; i < numHouses; i++) {
    house(t, 1.0/(1.0+i));
      }
    }

    public static void house(Turtle t, double scale) {
      front(t, scale);
      t.left(90);
      t.forward(80*scale);
      t.right(90);
      top(t, scale);
      t.left(90);
      t.backward(80*scale);
      t.right(90);
      t.penup();
      t.forward(80*scale +20);
      t.pendown();
    }

    public static void front(Turtle t, double scale) {
      walls(t, scale);
      t.forward(30*scale);
      door(t, scale);
      t.penup();
      t.left(90);
      t.forward(50*scale);
      t.right(90);
      t.backward(20*scale);
      t.pendown();
      windows(t, scale);
      t.penup();
      t.backward(10*scale);
      t.left(90);
      t.backward(50*scale);
      t.right(90);
      t.pendown();
    }

    public static void top(Turtle t, double scale) {
      roof(t, scale);
      t.penup();
      t.forward(10*scale);
      t.left(90);
      t.forward(10*scale);
      t.right(90);
      t.pendown();
      chimney(t, scale);
      t.penup();
      t.backward(10*scale);
      t.right(90);
      t.forward(10*scale);
      t.left(90);
      t.pendown();
    }

    public static void walls(Turtle t, double scale) {
      square(t, 80*scale);
    }

    public static void windows(Turtle t, double scale) {
      square(t, 20*scale);
      t.penup();
      t.forward(40*scale);
      t.pendown();
      square2(t, 20*scale);
      t.penup();
      t.backward(40*scale);
      t.pendown();
    }

    public static void door(Turtle t, double scale) {
      for (int i = 0; i < 2; i++) {
        t.forward(20*scale);
        t.left(90);
        t.forward(30*scale);
        t.left(90);
      }
    }

    public static void roof(Turtle t, double scale) {
      t.forward(80*scale);
      t.left(135);
      t.forward(40 * Math.sqrt(2) * scale);
      t.left(90);
      t.forward(40 * Math.sqrt(2) * scale);
      t.left(135);
    }

    public static void chimney(Turtle t, double scale) {
      t.left(90);
      t.forward(20*scale);
      t.right(90);
      t.forward(10*scale);
      t.right(90);
      t.forward(10*scale);
      t.backward(10*scale);
      t.left(90);
      t.backward(10*scale);
      t.left(90);
      t.backward(20*scale);
      t.right(90);
    }

    public static void square2(Turtle t, double x) {
      for (int i = 0; i < 4; i++) {
        t.forward(x);
        t.left(90);
      }
    }

}
