public class hw4 {
    public static void main(String[] args) {
        //1
        System.out.println(isReverse("happy", "yppah")); // will return true
        System.out.println(isReverse("cool", "loac")); // will return false
        System.out.println(isReverse("", ""));// will return true
        /*2
        Turtle wanting = new Turtle();
        turtleSpiral(wanting, 100, 10);
        */
        /*3
        Turtle vitaminc = new Turtle();
        vitaminc.delay(1);
        vitaminc.penup();
        vitaminc.backward(400);
        vitaminc.pendown();
        simpleFlower(vitaminc, 200);
        vitaminc.right(90);
        vitaminc.penup();
        vitaminc.forward(200);
        vitaminc.pendown();
        vitaminc.left(90);
        fractalFlower(vitaminc, 250, 3);
        vitaminc.penup();
        vitaminc.right(90);
        vitaminc.forward(200);
        vitaminc.left(90);
        vitaminc.pendown();
        fractalFlower(vitaminc, 300, 4);
        */

        /*4
        Turtle jang = new Turtle();
        jang.delay(0);
        //mickeyFace(jang, 50);
        fractalMickeyMouse(jang, 50, 5);

         */
        //5
        Turtle depression = new Turtle();
        depression.delay(1);
        levelArrows(depression, 50, 5);
    }

    //1
    public static boolean isReverse(String s1, String s2) {
        if (s1.length() != s2.length()) return false; //Makes sure that both strings are the same length.
        boolean result = true; //Starts with true.
        if (s1 == s2) {
            return result;
        } else {
            if(s1.charAt(0) != s2.charAt(s2.length()-1) || result == false){
                result = false; //Returns if a letter doesn't match.
                return result;
            } else {
                if (isReverse(s1.substring(1), s2.substring(0,s2.length()-1))== false) return false; //returns false if any letter doesn't match.
            }
        }
        return result;
    }

    //2
    public static void turtleSpiral(Turtle t, double size, double minSize) {
        if (size <= minSize){ //The base case is the iteration one step before minimum size.
            t.left(90);
            t.forward(minSize);
        } else {
            t.forward(size);
            t.left(90);
            turtleSpiral(t, 0.9 * size, minSize); //performs the recursion until the minimum threshold is hit.
        }
    }

    //3a
    public static void simpleFlower (Turtle t, double size) {
        t.left(90);
        t.forward(size);
        t.backward(size/3); //draws each line of the flower/
        for (int i = 0; i < 8; i++) { //repeats 8 times
            t.right(45);
            t.forward(size/3);
            t.backward(size/3);
        }
        t.backward(2*size/3); // ensures turtle goes back to original position
    }

    //3b
    public static void fractalFlower (Turtle t, double size, int level) {
        if (level == 0) {
            t.forward(size); //Base case must be a line as per assignment.
        } else if (level == 1) { // The real base case: the flower
            t.forward(size);
            t.backward(size/3);
            for (int i = 0; i < 8; i++) {
                t.right(45);
                t.forward(size/3);
                t.backward(size/3);
            }
            t.backward(2*size/3);
        } else { //repeats the base base 8 times per level.
                t.forward(size);
                t.backward(size/3);
            for(int i = 0 ; i<8; i++) {
                t.right(45);
                fractalFlower(t, size / 3, level - 1);
            }
            t.backward(2*size/3);
        }
    }

    //4
    public static void mickeyFace(Turtle t, double r) {//Draws a weird looking mouse.
        t.penup();
        t.backward(r);
        t.pendown(); //Much much turtle code to positive the images.
            polygon(t, 2 * r * Math.PI, 360);  //Eyes
            t.penup();
            t.right(90);
            t.forward(r/2);
            t.left(90);
            t.backward(r/2);
            t.pendown();
            polygon(t, r*0.5*Math.PI, 360);
            t.penup();
            t.forward(r/1.5);
            t.pendown();
            polygon(t, r*0.5*Math.PI, 360);//Nose
            t.penup();
            t.backward(r/3);
            t.right(90);
            t.forward(r/3);
            t.left(90);
            t.pendown();
            polygon(t, r,360);
            t.penup();
            t.backward(r/2);
            t.right(90);
            t.forward(r/4);
            t.left(90);
            t.forward(r/2);
            t.backward(r/2);
            t.pendown();
            t.right(90);
            for (int i = 0; i< 180; i++) {//Draws the mouth
                t.forward((r/2)*Math.PI/180);
                t.left(1);
            }
        t.penup(); //Repositions the turtle to avoid confusion later
            t.forward(r/2 + r/3 + r/4);
            t.right(90);
            t.backward(r/3);
        t.pendown();
    }

    public static void polygon(Turtle t, double size, int sides) {
        for (int i = 0; i < sides; i++) {
            t.forward(size/sides);
            t.right(360/sides);
        }
    }

    public static void fractalMickeyMouse (Turtle t, double r, int level) {
        if (level == 0) {
            mickeyFace(t, r); //Base mousey
        } else {
            mickeyFace(t, r); //Sets up the frame of the mouse fractal.
            t.penup();
            t.forward(1.5*r);
            t.right(90);
            t.backward(r/1.5);
            t.left(90);
            t.pendown();
            fractalMickeyMouse(t, 0.5*r, level -1);
            t.penup();
            t.backward(1.5*r);
            t.pendown(); //Before each new recursive command, prepares turtle in desired location
            fractalMickeyMouse(t, 0.5*r, level -1);
            t.penup(); // After each new recursive command, we return turtle to original location to avoid confusion later.
            t.forward(1.5*r);
            t.right(90);
            t.forward(r/1.5);
            t.left(90);
            t.backward(r/1.5);
            t.pendown();
        }
    }

    //5
    public static void levelArrows (Turtle t, double size, int level) {//Code that draws creative arrows.
        if (level == 0) { // base 0 case was established to draw normal arrows.
            colorchange(t); // Changes color when it enters base case.
            for (int j = 0; j < 8; j++) {
            t.forward(2*size);
            t.right(90);
            t.backward(0.5*size);
            for (int i = 0; i < 1; i++) { // Similar to recursive code, but level was changed to 1 because divide by 0 is invalid.
                t.forward(size);
                t.left(360/1);
                }
            for (int f = 0; f < 1; f++) {
                t.right(360/1);
                t.backward(size);
            }
            t.forward(0.5*size);
            t.left(90);
            t.backward(2*size);
            t.left(45);
            }
        } else {
                colorchange(t);//Changes color when on every level.
                for (int j = 0; j < 8; j++) {
                    t.forward(2*size);
                    t.right(90);
                    t.backward(0.5*size);
                    for (int i = 0; i < level; i++) {//Draws an unique polygon for each level of the fractal.
                        t.forward(size);
                        t.left(360/level);
                    }
                    for (int f = 0; f < level; f++) {
                        t.right(360/level);
                        t.backward(size);
                    }
                    t.forward(0.5*size);
                    t.left(90);
                    t.backward(2*size);
                    t.left(45);
                }
                t.penup();
                t.forward(size/2);
                t.pendown();
                levelArrows(t, size, level -1); //Each level is comprise of the last level sandwhiching the lower level.
                for ( int j = 0; j < 8; j++) {//The code below is just a repeat of the code above.
                    t.forward(2*size);
                    t.right(90);
                    t.backward(0.5*size);
                    for (int i = 0; i < level; i++) {
                        t.forward(size);
                        t.left(360/level);
                    }
                    for (int f = 0; f < level; f++) {
                        t.right(360/level);
                        t.backward(size);
                    }
                    t.forward(0.5*size);
                    t.left(90);
                    t.backward(2*size);
                    t.left(45);
                }
                t.penup();
                t.forward(size/2);
                t.pendown();
        }
    }

    public static void colorchange (Turtle t){//Changing color method.
        int min = 0;
        int max = 255;
        double a = Math.random()*(max-min+1)+min;
        double b = Math.random()*(max-min+1)+min;
        double c = Math.random()*(max-min+1)+min;
        int d = (int)a;
        int e = (int)b;
        int f = (int)c;
        t.color(d,e,f);
    }
}