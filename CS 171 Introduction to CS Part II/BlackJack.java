/* Microl Chen
microl.chen@emory.edu ~ tche284

THIS CODE WAS MY OWN WORK , IT WAS WRITTEN WITHOUT CONSULTING ANY
SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR. - Microl Chen
*/

import java.util.ArrayList;
import java.util.Random;
import javax.swing.JOptionPane;

public class BlackJack {
    // fill in code here
    // define data members
    
    public static void buildDeck(ArrayList<Card> deck) {
	// fill in code here
	// Given an empty deck, construct a standard deck of playing cards

		for (int r = 1; r < 14; r++) {
			for (int i = 0; i < 4; i++) {
				Card cards = new Card();
				deck.add(cards);
				cards.assign(r);
			}
		}

    }

    public static void initialDeal(ArrayList<Card> deck, ArrayList<Card> playerHand, ArrayList<Card> dealerHand){
	// fill in code here
	// Deal two cards from the deck into each of the player's hand and dealer's hand
		playerHand.clear();
		dealerHand.clear();

		dealOne(deck,playerHand);
		dealOne(deck,dealerHand);
		dealOne(deck,playerHand);
		dealOne(deck,dealerHand);

    }

    public static void dealOne(ArrayList<Card> deck, ArrayList<Card> hand){
	// fill in code here
	// this should deal a single card from the deck to the hand
		Random rand = new Random();
		int cc = 51;
		int upperbound = cc;
		//generate random values from currentcount.

		Card cards = new Card();
		int randomnumber = rand.nextInt(upperbound);
		cards = deck.get(randomnumber);
		hand.add(cards);
		deck.remove(rand);
		cc --;

    }

    public static boolean checkBust(ArrayList<Card> hand){
	// fill in code here
	// This should return whether a given hand's value exceeds 21
		int handsize = hand.size();
		int handvalue = 0;
		int ace_count = 0;
		for (int i = 0; i < hand.size(); i++) {
			if (hand.get(i).value != 11) { handvalue += hand.get(i).value;
			} else {
				handvalue += 11;
				ace_count++;
				}
			}
		//Ace exceptions
		while (handvalue > 21 && ace_count != 0) {
			ace_count --;
			handvalue -= 10;
		}
		if (handvalue > 21 && ace_count == 0) return true;
		return false;
    }

    public static boolean dealerTurn(ArrayList<Card> deck, ArrayList<Card> hand){
	// fill in code here
	// This should conduct the dealer's turn and
	// Return true if the dealer busts; false otherwise

		int handsize = hand.size();
		int handvalue = 0;
		int ace_count = 0;
		for (int i = 0; i < hand.size(); i++) {
			if (hand.get(i).value != 11) {
				handvalue += hand.get(i).value;
			} else {
				handvalue += 11;
				ace_count ++;
			}
		}

		//Ace exceptions & Hit if below 17

		while ((handvalue > 21 && ace_count != 0) || handvalue < 17) {
			if (handvalue > 21 && ace_count != 0) {
				ace_count--;
				handvalue -= 10;
			} else if (handvalue < 17) {
				dealOne(deck, hand);
				handsize = hand.size();
				handvalue = 0;
				for (int i = 0; i < hand.size(); i++) {
					if (hand.get(i).value != 11) handvalue += hand.get(i).value;
					if (hand.get(i).value == 11) {
						handvalue += 11;
						ace_count ++;
					}
				}
			}
		}

		if (handvalue > 21 && ace_count == 0) return true;
	return false;
    }

    public static int whoWins(ArrayList<Card> playerHand, ArrayList<Card> dealerHand){
	// fill in code here
	// This should return 1 if the player wins and 2 if the dealer wins
		int handsizePlayer = playerHand.size();
		int handvaluePlayer = 0;
		for (int i = 0; i < playerHand.size(); i++) {
			handvaluePlayer += playerHand.get(i).value;
		}

		int handsizeDealer = dealerHand.size();
		int handvalueDealer = 0;
		for (int i = 0; i < dealerHand.size(); i++) {
			handvalueDealer += dealerHand.get(i).value;
		}

		if (handvalueDealer >= handvaluePlayer && handvalueDealer <= 21) return 2;
		if (handvaluePlayer > handvalueDealer && handvaluePlayer <= 21) return 1;

	return 0;
    }

    public static String displayCard(ArrayList<Card> hand){
	// fill in code here
	// Return a string describing the card which has index 1 in the hand
		String cardName = hand.get(1).name;
		int cardValue = hand.get(1).value;
		String description = " a " + cardName + ", with a card value of " +cardValue+ ".";
		return description;
    }

    public static String displayHand(ArrayList<Card> hand){
	// fill in code here
	// Return a string listing the cards in the hand
		String cardsInHand = "";
		int temp = hand.size()-1;

		for (int i = 0; i < temp; i++) {
			cardsInHand += hand.get(i).name + ", ";
			}
		cardsInHand += hand.get(temp).name;
		return cardsInHand;
    }

    // fill in code here (Optional)
    // feel free to add methods as necessary


    public static void main(String[] args) {
		int playerChoice, winner;
		ArrayList<Card> deck = new ArrayList<Card>();
		
		playerChoice = JOptionPane.showConfirmDialog(
			null, 
			"Ready to Play Blackjack?", 
			"Blackjack", 
			JOptionPane.OK_CANCEL_OPTION
		);

		if((playerChoice == JOptionPane.CLOSED_OPTION) || (playerChoice == JOptionPane.CANCEL_OPTION))
		    System.exit(0);
		
		Object[] options = {"Hit","Stand"};
		boolean isBusted;	// Player busts? 
		boolean dealerBusted;
		boolean isPlayerTurn;
		ArrayList<Card> playerHand = new ArrayList<>();
		ArrayList<Card> dealerHand = new ArrayList<>();
	
		do{ // Game loop
			buildDeck(deck);  // Initializes the deck for a new game
		    initialDeal(deck, playerHand, dealerHand);
		    isPlayerTurn=true;
		    isBusted=false;
		    dealerBusted=false;
		    
		    while(isPlayerTurn){

				// Shows the hand and prompts player to hit or stand
				playerChoice = JOptionPane.showOptionDialog(
					null,
					"Dealer shows " + displayCard(dealerHand) + "\n Your hand is: " 
						+ displayHand(playerHand) + "\n What do you want to do?",
					"Hit or Stand",
				   JOptionPane.YES_NO_OPTION,
				   JOptionPane.QUESTION_MESSAGE,
				   null,
				   options,
				   options[0]
				);

				if(playerChoice == JOptionPane.CLOSED_OPTION)
				    System.exit(0);
				
				else if(playerChoice == JOptionPane.YES_OPTION){
				    dealOne(deck, playerHand);
				    isBusted = checkBust(playerHand);
				    if(isBusted){
						// Case: Player Busts
						playerChoice = JOptionPane.showConfirmDialog(
							null,
							"Player has busted!", 
							"You lose", 
							JOptionPane.OK_CANCEL_OPTION
						);

						if((playerChoice == JOptionPane.CLOSED_OPTION) || (playerChoice == JOptionPane.CANCEL_OPTION))
						    System.exit(0);
						
						isPlayerTurn=false;
				    }
				}
			    
				else{
				    isPlayerTurn=false;
				}
		    }

		    if(!isBusted){ // Continues if player hasn't busted
				dealerBusted = dealerTurn(deck, dealerHand);
				if(dealerBusted){ // Case: Dealer Busts
				    playerChoice = JOptionPane.showConfirmDialog(
				    	null, 
				    	"The dealer's hand: " +displayHand(dealerHand) + "\n \n Your hand: " 
				    		+ displayHand(playerHand) + "\nThe dealer busted.\n Congrautions!", 
				    	"You Win!!!", 
				    	JOptionPane.OK_CANCEL_OPTION
				    );		    

					if((playerChoice == JOptionPane.CLOSED_OPTION) || (playerChoice == JOptionPane.CANCEL_OPTION))
						System.exit(0);
				}
			
			
				else{ //The Dealer did not bust.  The winner must be determined
				    winner = whoWins(playerHand, dealerHand);

				    if(winner == 1){ //Player Wins
						playerChoice = JOptionPane.showConfirmDialog(
							null, 
							"The dealer's hand: " +displayHand(dealerHand) + "\n \n Your hand: " 
								+ displayHand(playerHand) + "\n Congrautions!", 
							"You Win!!!", 
							JOptionPane.OK_CANCEL_OPTION
						);

						if((playerChoice == JOptionPane.CLOSED_OPTION) || (playerChoice == JOptionPane.CANCEL_OPTION))
						    System.exit(0);
				    }

				    else{ //Player Loses
						playerChoice = JOptionPane.showConfirmDialog(
							null, 
							"The dealer's hand: " +displayHand(dealerHand) + "\n \n Your hand: " 
								+ displayHand(playerHand) + "\n Better luck next time!", 
							"You lose!!!", 
							JOptionPane.OK_CANCEL_OPTION
						); 
					
						if((playerChoice == JOptionPane.CLOSED_OPTION) || (playerChoice == JOptionPane.CANCEL_OPTION))
						    System.exit(0);
				    }
				}
		    }
		}while(true);
    }
}



class Card {
	// Specify data fields for an individual card
	public String name;
	public int value;
	public void assign(int x){
		if (x == 1) {setName("ACE");}
		if (x == 2) {setName("Two");}
		if (x == 3) {setName("Three");}
		if (x == 4) {setName("Four");}
		if (x == 5) {setName("Five");}
		if (x == 6) {setName("Six");}
		if (x == 7) {setName("Seven");}
		if (x == 8) {setName("Eight");}
		if (x == 9) {setName("Nine");}
		if (x == 10) {setName("Ten");}
		if (x == 11) {setName("Jack");}
		if (x == 12) {setName("Queen");}
		if (x == 13) {setName("King");}
		if (x < 11 && x != 1) {setValue(x);}
		if (x > 10) {setValue(10);}
		if (x == 1) {setValue(11);}
	}
	public void setName(String name){
		this.name = name;
	}
	public void setValue(int v){
		this.value = v;
	}
	Card(){
		// Fill in constructor method
	}
}