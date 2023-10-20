/* Microl Chen
microl.chen@emory.edu ~ tche284

THIS CODE WAS MY OWN WORK , IT WAS WRITTEN WITHOUT CONSULTING ANY
SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR. - Microl Chen
*/

/**
 * Starter code for the Maze path finder problem.
 */

import java.io.*;
import java.util.Scanner;
import java.util.ArrayDeque;
import java.util.Stack;
import java.util.Queue;
import java.util.*;

/*
 * Recursive class to represent a position in a path
 */
class Position{
	public int i;     //row
	public int j;     //column
	public char val;  //1, 0, or 'X'

	// reference to the previous position (parent) that leads to this position on a path
	Position parent;

	Position(int x, int y, char v){
		i=x; j = y; val=v;
	}

	Position(int x, int y, char v, Position p){
		i=x; j = y; val=v;
		parent=p;
	}

	public void seti (int i) {
		this.i = i;
	}
	public void setj (int j) {
		this.j = j;
	}
	public void setParent (Position p) {
		this.parent = p;
	}
	public void setval (char val) {
		this.val = val;
	}

}


public class PathFinder {

	public static void main(String[] args) throws IOException {

		if(args.length<1){
			System.err.println("***Usage: java PathFinder maze_file");
			System.exit(-1);
		}

		char [][] maze;
		maze = readMaze(args[0]);
		printMaze(maze);
		Position [] path = stackSearch(maze);
		System.out.println("stackSearch Solution:");
		printPath(path);
		printMaze(maze);

		char [][] maze2 = readMaze(args[0]);
		path = queueSearch(maze2);
		System.out.println("queueSearch Solution:");
		printPath(path);
		printMaze(maze2);
	}


	public static Position [] stackSearch(char [] [] maze){
		// todo: your path finding algorithm here using the stack to manage search list
		// your algorithm should mark the path in the maze, and return array of Position
		// objects coressponding to path, or null if no path found

		int n = maze.length;
		Stack<Position> searchList = new Stack<Position>();
		Stack<Position> path = new Stack<Position>();

		Position start = new Position(0,0,'0');
		searchList.push(start); //adds initial position

		int[][] memory = new int[maze.length][maze.length]; //Keeps track of visited locations.

		int count =0;
		int precount =1;
		int a = 0;
		int b = 0;
		int c = 0;
		int d = 0;

		while (searchList.empty() == false) { //Main while loop that runs until all visited or solution is found.
			Position temp = searchList.pop();
			Position parent = new Position(temp.i,temp.j,'0',temp.parent); //Creates the parent of current position

			a = temp.i;
			b = temp.j;


			if (temp.i == n-1 && temp.j == n-1) { //If ending is found
				path.push(temp);
				c = 10;
				d = 10;
				while (!(c == 0 && d == 0)) {//We count the number of positions (or steps)
					c = temp.parent.i;
					d = temp.parent.j;
					temp = temp.parent;
					path.push(temp); //while pushing the positions into another stack
					precount++;
				}

				c = 100;
				d = 100;

				Position[] result = new Position[precount+1];

				while (path.empty() == false) { //Creates the position array with the stack of the path.
					Position temp22 = path.pop();
					temp22.setval('X');
					result[count] = temp22;
					count++;
					maze[temp22.i][temp22.j] = 'X';
				}
				return result;

			} else {//Checks possible movements
				//if it is possible to go up, push the up position into stack etc, for all four cardinal directions.
				//Also records visited locations into memory.
				final int up = a-1;
				final int up2 = b;
				final int down = a+1;
				final int down2 = b;
				final int left = a;
				final int left2 = b-1;
				final int right = a;
				final int right2 = b+1;

				if (up >= 0 && up <n && up2 >= 0 && up2 <n) {
					if (maze[up][up2] == '0' && memory[up][up2] != 1) {

						Position dup = new Position(0,0, '0');
						dup.setParent(parent);
						dup.seti(up);
						dup.setj(up2);
						searchList.push(dup);
						memory[up][up2] = 1;

					}
				}


				if (down >= 0 && down <n && down2 >= 0 && down2 <n) {
					if (maze[down][down2] == '0' && memory[down][down2] != 1) {
						Position ddown = new Position(0,0, '0');
						ddown.setParent(parent);
						ddown.seti(down);
						ddown.setj(down2);
						searchList.push(ddown);
						memory[down][down2] = 1;

					}
				}


				if (right >= 0 && right <n && right2 >= 0 && right2 <n) {
					if (maze[right][right2] == '0' && memory[right][right2] != 1) {
						Position dright = new Position(0,0, '0');
						dright.setParent(parent);
						dright.seti(right);
						dright.setj(right2);
						searchList.push(dright);
						memory[right][right2] = 1;
					}
				}


				if (left >= 0 && left <n && left2 >= 0 && left2 <n) {
					if (maze[left][left2] == '0' && memory[left][left2] != 1) {
						Position dleft = new Position(0,0, '0');
						dleft.setParent(parent);
						dleft.seti(left);
						dleft.setj(left2);
						searchList.push(dleft);
						memory[left][left2] = 1;
					}
				}

			}
		}
		System.out.println();
		System.out.println("There is no Path");
		return null;
	}

	public static Position [] queueSearch(char [] [] maze){
		// todo: your path finding algorithm here using the queue to manage search list
		// your algorithm should mark the path in the maze, and return array of Position
		// objects coressponding to path, or null if no path found

		//Very much same with Stacks. **********
		int n = maze.length;
		Queue<Position> searchList = new LinkedList<Position>();
		Queue<Position> path = new LinkedList<Position>();

		Position start = new Position(0,0,'0');
		searchList.add(start);

		int[][] memory = new int[maze.length][maze.length];
		int count =0;
		int precount =1;
		int a = 0;
		int b = 0;
		int c = 0;
		int d = 0;

		while (searchList.isEmpty() == false) { //removes locations from queue
			Position temp = searchList.remove();
			Position parent = new Position(temp.i,temp.j,'a',temp.parent);
			a = temp.i;
			b = temp.j;

			if (temp.i == n-1 && temp.j == n-1) { //if it is the ending location, counts the number of steps (parents)
				path.add(temp);
				c = 10;
				d = 10;
				while (!(c == 0 && d == 0)) {//Adds the parents into another queue
					c = temp.parent.i;
					d = temp.parent.j;
					temp = temp.parent;
					path.add(temp);
					precount++;
				}

				c = 100;
				d = 100;

				Position[] result = new Position[precount+1];

				count = precount-1;

				while (path.isEmpty() == false) {//using the list of position of steps, construct the position array
					Position temp22 = path.remove();
					temp22.setval('X');
					result[count] = temp22;
					count--;
					maze[temp22.i][temp22.j] = 'X';
				}
				return result;

			} else { //if it is not the ending position, check all four possible moves

				final int up = a-1;
				final int up2 = b;
				final int down = a+1;
				final int down2 = b;
				final int left = a;
				final int left2 = b-1;
				final int right = a;
				final int right2 = b+1;
				//If a location is possible to move, add into search queue, set memory as visted,

				if (up >= 0 && up <n && up2 >= 0 && up2 <n) {
					if (maze[up][up2] == '0' && memory[up][up2] != 1) {
						Position dup = new Position(0,0, 'a');
						dup.setParent(parent); //remember to set parent
						dup.seti(up);
						dup.setj(up2);
						searchList.add(dup);
						memory[up][up2] = 1;

					}
				}


				if (down >= 0 && down <n && down2 >= 0 && down2 <n) {
					if (maze[down][down2] == '0' && memory[down][down2] != 1) {
						Position ddown = new Position(0,0, 'a');
						ddown.setParent(parent);
						ddown.seti(down);
						ddown.setj(down2);
						searchList.add(ddown);
						memory[down][down2] = 1;

					}
				}


				if (right >= 0 && right <n && right2 >= 0 && right2 <n) {
					if (maze[right][right2] == '0' && memory[right][right2] != 1) {
						Position dright = new Position(0,0, 'a');
						dright.setParent(parent);
						dright.seti(right);
						dright.setj(right2);
						searchList.add(dright);
						memory[right][right2] = 1;
					}
				}


				if (left >= 0 && left <n && left2 >= 0 && left2 <n) {
					if (maze[left][left2] == '0' && memory[left][left2] != 1) {
						Position dleft = new Position(0,0, 'a');
						dleft.setParent(parent);
						dleft.seti(left);
						dleft.setj(left2);
						searchList.add(dleft);
						memory[left][left2] = 1;
					}
				}

			}
		}
		System.out.println();
		System.out.println("There is no Path");
		return null;
	}

	public static void printPath(Position [] path){//Prints a position array for the path
		// todo: print the path to the stdout
		System.out.print("Path: (");
		for (int o = 0; o < path.length-1; o++) {
			if (o <path.length -2) System.out.print("["+ path[o].i+"]["+path[o].j+"], ");
			if (o == path.length-2) System.out.print("["+path[o].i+"]["+path[o].j+"]");
		}
		System.out.print(")");
		System.out.println();
	}

	/**
	 * Reads maze file in format:
	 * N  -- size of maze
	 * 0 1 0 1 0 1 -- space-separated
	 * @param filename
	 * @return
	 * @throws IOException
	 */
	public static char [][] readMaze(String filename) throws IOException{
		char [][] maze;
		Scanner scanner;
		try{
			scanner = new Scanner(new FileInputStream(filename));
		}
		catch(IOException ex){
			System.err.println("*** Invalid filename: " + filename);
			return null;
		}

		int N = scanner.nextInt();
		scanner.nextLine();
		maze = new char[N][N];
		int i=0;
		while(i < N && scanner.hasNext()){
			String line =  scanner.nextLine();
			String [] tokens = line.split("\\s+");
			int j = 0;
			for (; j< tokens.length; j++){
				maze[i][j] = tokens[j].charAt(0);
			}
			if(j!=N){
				System.err.println("*** Invalid line: " + i + " has wrong # columns: " + j);
				return null;
			}
			i++;
		}
		if(i!=N){
			System.err.println("*** Invalid file: has wrong number of rows: " + i);
			return null;
		}
		return maze;
	}

	public static void printMaze(char[][] maze){

		if(maze==null || maze[0] == null){
			System.err.println("*** Invalid maze array");
			return;
		}

		for(int i=0; i< maze.length; i++){
			for(int j = 0; j< maze[0].length; j++){
				System.out.print(maze[i][j] + " ");
			}
			System.out.println();
		}

		System.out.println();
	}

}
