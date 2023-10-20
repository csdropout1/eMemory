public class HW2 {

  public static void main(String[] args) {
    /* 1
    int a = sumOfSquares(4);
    int b = product(8, 9);
    double c = compundInterest(1000, 0.05, 3);
    double d = polySpiralLength(3, 10, 3);
    System.out.println(a);
    System.out.println(b);
    System.out.println(c);
    System.out.println(d); */

    /* 2
    String deci = decimalToBinary(23);
    System.out.println(deci);
     */

     //3
    //Task 2, We want Car B for both.
    //Task 3, Printing something tells terminal to actually print it, while returning
    //a value only assigns it to a variable outside of the method.
    //This is why we still have to print it after we return a variable to the main.
    String comparecars = compareCars(5);
    System.out.println(comparecars);

     //4
    /*String story = storyteller("Alice", "Rose", "diamonds", 10,
            "pigs", "enemies","unhappy");
    System.out.println(story);

    //int a = letterCount("cattle", "");
    //System.out.println(a);

    //int a = digitCount(0, 0);
    //System.out.println(a);

    int a = wordCount("  Why dfis   this guy iq");
    System.out.println(a);*/
  }

  //Problem 1 "Some Maths"
//a
  public static int sumOfSquares(int n) {//takes a positive integer n and returns the sum of the squares from
    //  1^2 up to n^2, input n is the last value that is square, and the output is the sum.
    int result = 0; // initialize result
    for (int i = 1; i <= n; i++) { //uses forloop to multiple each value up to n, and add it to the result.
      result += i * i;
    }
    return result;
  }

  //b
  public static int product(int x, int y) {//Takes the product of input x and y.
    int product = 0; // initialize
    for (int i = 0; i < x; i++) { // Adds y to itself x amount of times.
      product += y;
    }
    return product;
  }

  //c
  public static double compundInterest(double money, double interestRate, int years) {
    //Calculates compound interest given initial money, a fixed interest rate, and the duration.
    for (int i = 1; i <= years; i++) { //adds the interest for each year
      money *= (1 + interestRate);
    }
    return money;
  }

  //d
  public static double polySpiralLength(int n, double base, int rounds) {
    //Computes the total length of a polyspiral:
    double length = 0;
    for (int i = 1; i <= rounds; i++) { //Each round has a length that is one base more than previous
      length += i * base; //So we accumulate each length
    }
    return length; //notice n does not matter, as that only affects the angle and not the actual length.
  }


  //Problem 2: Decimal to Binary
  public static String decimalToBinary(int n) { //converts a number between 0 to 255 into binary.
    String binary = "";
    for (int i = 0; i < 8; i++) { //since number is <256, we have 8 total 0s or 1s.
      if (n >= Math.pow(2, (7 - i))) { //start with 2^7, which is 128, we can reduce the initial value of n and add
        n -= Math.pow(2, (7 - i)); //either a 1 or 0 depending if n is greater than the deduction amount.
        binary += "1"; // adds 1 to the nth slot if current value can subtract 2^n
      } else {
        binary += "0"; //adds 0 otherwise and move on to next slot.
      }
    }
    return binary;
  }

  //Problem 3: Let's buy a new car
  //Task 1:
  public static String compareCars(int years) { //Picks the more economical car
    //given the years of intended ownership.
    double totala = 20000; //initial costs
    double totalb = 30000;
    double gasA = (15000 / 25); //gas cost/year
    double gasB = (15000 / 32);
    for (int i=0; i<= years; i++){ //Accumulates total costs
      double a = maintence(i, true); //boolean values used to direct what values to return.
      double b = maintence(i, false);
      totala += (i*gasA*2.5) + a;
      totalb += (i*gasB*2.5) + b;
      System.out.println("Year "+ i + "\tCost A "+totala+ "\tCost B "+totalb);
    } //Prints each iteration into a makeshift table.
    if (totala < totalb) { //returns the car that costs the lower value.
      return "Car A";
    } else {
      return "Car B";
    }
  }
    public static double maintence(int years, boolean x){
      if (years == 0) {//No maintenance when 0 years has passed.
        return 0;
      }
      double mainA = 1300; //initial maintenence
      double mainB = 1000;
      for (int i=1; i<years; i++) { //Accumulation of cost AND compound interest
        mainA += (1 + 0.15)*mainA;
        mainB += (1 + 0.10)*mainB;
      }
      if (x == true) { //returns values to correct place.
        return mainA;
      } else {
        return mainB;
      }
  }
//Problem 4: The storyteller
  public static String storyteller(String name1, String name2, String item, int quan, String item2
  , String relation, String emotion){ //construct a story with given strings.
    int sad = quan/2;
    int lengthname1 = name1.length()-1;
    char x = name1.charAt(lengthname1); //last letter first girl
    int lengthname2 = name2.length()-1;
    char y = name2.charAt(lengthname2); //last letter second girl
    char xx = name1.charAt(0); //Fist letter first girl
    char yy = name2.charAt(0); //Fist letter second girl
    int lengthitem = item.length()-1;
    char z = item.charAt(lengthitem); //Last letter of item envy
    char zz = item.charAt(0); // First letter of object
    String xxx = ""+x; ///Change to string
    String upperx = xxx.toUpperCase(); //Uppercase
    String yyy = ""+yy;
    String loweryy = yyy.toLowerCase();
    String xxxx = ""+xx;
    String lowerxx = xxxx.toLowerCase();
    String cursedpart1 = upperx+"aa"+lowerxx+" "+y+"ee"+loweryy+" "+z+"ii"+zz+"!"; //Develop spell
    String cursedpart2 = cursedpart1.toUpperCase(); //All caps spells
    String cursed = cursedpart1+" "+cursedpart2; //combine
    String story = ""+name1+" was a beautiful princess. "+name2+" was a wicked witch. "+
          name1+" had "+quan+" expensive "+item+", whereas "+name2+" had only "+sad+
          ". Because of envy, "+name2+" cast a spell on "+name1+", yelling these arcane magical words:"+
          "\""+cursed+"\". Suddenly, "+name1+"'s "+quan+" "+item+" turned into "+item2+". "
          +name1+" became very "+emotion+". Seeing that "+name1+" was "+emotion+", "+name2+" realized she was wrong"+
          " and reversed the spell. "+name1+" and "+name2+" became "+relation+", and they lived happily ever after.";
    return story;
  }

//Problem 5: Letter count
  public static int letterCount(String s, String c){ //counts the iterations of c in s.
    if (s == "" || c == "") { //Error situations address
      return 0;
    }
    int count = 0; //initialize
    char d = c.charAt(0); //change string to character
    for (int i=1; i<=s.length(); i++){ //loop through each char in s.
      char x = s.charAt(i-1);
      if (x == d) { //counts the char if it is identical to c.
        count++;
      }
    }
    return count;
  }

//Problem 6 Digit count
  public static int digitCount (int number, int digit){ //determines the amount of digits in a number.
    int m = number;
    int numDigits =0;
    while (m > 10) {  //This helps us counts how "long" the number is.
      numDigits++;
      m = m/10;
    }
    numDigits ++;
    int count = 0;
    for (int i=numDigits; i> 0; i--){ // We do this for each of the digits.
      double b = identify(number, Math.pow(10,i));
      number -= Math.pow(10,i)* b;
      int a = (int)b;
      if (a == digit){ // We count the digit if the digit is the one we are looking for.
        count++;
      }
    }
    return count;
    }

    public static int identify(int number, double location){//identifys the digit in each location.
      int digitID = 0;
      while (number >= location) { //Using the number's length, we can identify the number by subtracting
        number -= location; //an x amount from it to determine the digit.
        digitID++;
      }
      return digitID;
    }
//Problem 7 Word count
  public static int wordCount(String a){//counts the number of words in string a.
    int count =0;
    for (int i=0; i< a.length()-1;i++){ // We count each space followed by a character.
      if (a.charAt(i) == ' ' && a.charAt(i+1) != ' ') {
        count++;
      }
    }
    if (a.charAt(0) == ' ') {count--;} //We must subtract one if we began with a space due to following line.
    count ++; //We add one because the first word does not necessarily have a space in front of it.
    return count;
  }


}