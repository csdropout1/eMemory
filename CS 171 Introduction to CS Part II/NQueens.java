/* Microl Chen
microl.chen@emory.edu ~ tche284

THIS CODE WAS MY OWN WORK , IT WAS WRITTEN WITHOUT CONSULTING ANY
SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR. - Microl Chen
*/

import java.util.Stack;

public class NQueens {
  //***** fill in your code here *****
  //feel free to add additional methods as necessary

  //checks for diagonal cases
  public static boolean statuscheck(int row, int col, int n, Stack<Integer> xx, Stack<Integer> yy) {
    int[][] memory = new int[n][n];
    for (int i = 0; i< xx.size(); i++) {
      memory[xx.get(i)][yy.get(i)] = 1;
    }
    //made a 2D array for memory of where queens, could have also just use the stack but it was easier to read.

    int tr = 0;
    int tl = 0;
    int x = row;
    int y = col;
    int z = n - 1;
    boolean done = false;

    //just need to check top right and top left diagonals, as we are placing queens from top to bottom.
    //right top diagonal
    if (x == 0 || y == z) {
      done = true;
    } else {
      while (done == false) {
        tr ++;
        x --;
        y ++;
        if (x == 0 || y == z) done = true;
      }
    } //counts how many squares I need to check
    done = false;
    x = row;
    y = col;
    for (int i = 0; i < tr; i++) {
      x -= 1;
      y += 1;
      if (memory[x][y] == 1) return false;
    } // Checks the squares
    x = row;
    y = col;
    tr = 0;

    //left top diagonal *same with other diagonal
    if (x == 0 || y == 0) {
      done = true;
    } else {
      while (done == false) {
        tl ++;
        x --;
        y --;
        if (x == 0 || y == 0) done = true;
      }
    }
    done = false;
    x = row;
    y = col;
    for (int i = 0; i < tl; i++) {
      x -= 1;
      y -= 1;
      if (memory[x][y] == 1) return false;
    }
    x = row;
    y = col;
    tl = 0;

      return true;
    }
    //just a method to check if a queen's column position *aka solution* is already in stack
    //this is great as this automatically eliminates vertical attacks on queens.
  public static boolean inStack(Stack<Integer> s, int a) {
    boolean result = false;
    for (int i = 0; i < s.size(); i++) {
      if (a == s.get(i)) result = true;

    }
    return result;
  }
  //finds and prints out all solutions to the n-queens problem
  public static int solve(int n) {

    //***** fill in your code here *****
    boolean done = false;
    boolean rowDone = false;
    boolean status = false;
    int found = 0;
    boolean total = false;
    int pop = 0;
    boolean popcase = false;
    boolean temp = false;
    Stack<Integer> solution = new Stack<Integer>(); // column positions *asked by assignment
    Stack<Integer> rowmemory = new Stack<Integer>(); //made one for rows too just for ease of access
    int col = 0;
    int row = 0;
    boolean empty = false;

    while (done == false || total == false) {//this is the game loop that runs until all placements are tried.
      if (popcase == true) {//removes queens on the board when all possible current locations are not possible.
        row--;
        pop = solution.pop();
        rowmemory.pop();
        if (pop == n - 1) { //edge cases (need to remove two queens)
          row--;
          empty = solution.empty();
          if (empty) { //when all the positions are tried, it will try to remove a queen from empty stack, and this ends the while loop.
            return found;
            }
          pop = solution.pop();
          rowmemory.pop();
          col = pop + 1;
          popcase = false;
          pop = 0;
        } else { //normal case
          col = pop + 1;
          popcase = false;
          pop = 0;
        }
      } else {
        while (row < n && popcase == false) {//We must place a queen in every row, this ends when we have enough rows.
          rowDone = false;
          status = false;

          while (((col != n - 1) || rowDone == false) && popcase == false) {//We try a queen on every column until one works.
            if (inStack(solution, col) == true) {
              rowDone = true;
              status = true;
              col++;
              done = false;
            }
            if (rowDone == false || status == false) {
              if (col == n) {//if we reach the last column and we can not place queen, we must remove previous queen.
                popcase = true;
              } else {
                status = statuscheck(row, col, n, rowmemory, solution);

                if (status == true) {//Decides whether or not to place a queen or try the next square.
                  solution.add(col);
                  rowmemory.add(row);
                  if (rowmemory.size() == n && solution.size() == n) {//Checks if it is a complete solution.
                    found ++;
                    printSolution(solution);
                  }
                  col = 0; //resets into the next row.
                  rowDone = true;
                  row++;
                  status = false;
                } else {
                  col++;
                  if (col == n) {
                    popcase = true;
                  }
                }
              }
            }
            rowDone = false;
          }
        }
      }
    }
    //update the following statement to return the number of solutions found
    return found;
    //solve()
  }

  //this method prints out a solution from the current stack
  //(you should not need to modify this method)
  private static void printSolution(Stack<Integer> s) {
    System.out.println();
    for (int i = 0; i < s.size(); i++) {
      for (int j = 0; j < s.size(); j++) {
        if (j == s.get(i))
          System.out.print("Q ");
        else
          System.out.print("* ");
      }//for
      System.out.println();
    }//for
    System.out.println();
  }//printSolution()


  // ----- the main method -----
  // (you shouldn't need to change this method)
  public static void main(String[] args) {

    int n = 8;

    // pass in parameter n from command line
    if (args.length == 1) {
      n = Integer.parseInt(args[0].trim());
      if (n < 1) {
        System.out.println("Incorrect parameter");
        System.exit(-1);
      }//if
    }//if

    int number = solve(n);
    System.out.println("There are " + number + " solutions to the " + n + "-queens problem.");
  }//main()
}
