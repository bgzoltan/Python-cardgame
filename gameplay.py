# HUNGARIAN CARD GAME v.1.0

import cv2
import time
import textwrap
import shutil
from random import shuffle, choice

round_start=True
start_player='computer'
seven_cards=['A7', 'R7', 'G7', 'P7']
valuable_cards=['A10','R10','G10','P10','AA','RA','GA','PA']
abc='abcdefghijklmnopqrstuvwxyz'+'abcdefghijklmnopqrstuvwxyz'.upper()

def print_card(player,card,index):
    # displaying computer card, user card, and cards are in user's hand in windows
    # *** CV2 VERSION
    # Image loading
    name=str(player)+'-'+str(card)
    image = cv2.imread(f'Python-cardgame/cards/{deck.card_map[card]}.png')

    # Create a window 
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)

    # Set the window size / does not work properly / cannot let to decrease to the size of the image
    cv2.resizeWindow(name, 91, 146)  
    cv2.imshow(name, image)

    # Display the image
    if (player=='H'):
        cv2.moveWindow(name, 400, int(index)*170) 
    elif (player)=='U':
        cv2.moveWindow(name, 200, int(index)*170) 
    else:
        cv2.moveWindow(name, 0, int(index)*170) 

    # Not to hide the images
    cv2.waitKey(1)

class Deck():
    def __init__(self):
          self.card_map={'P7':'pumpkinseven','P8':'pumpkin-eight','P9':'pumpkin-nine','P10':'pumpkin-ten','PL':'pumpkin-lower','PU':'pumpkin-upper','PK':'pumpkin-king','PA':'pumpkin-ace','A7':'acorn-seven','A8':'acorn-eight','A9':'acorn-nine','A10':'acorn-ten','AL':'acorn-lower','AU':'acorn-upper','AK':'acorn-king','AA':'acorn-ace','R7':'red-seven','R8':'red-eight','R9':'red-nine','R10':'red-ten','RL':'red-lower','RU':'red-upper','RK':'red-king','RA':'red-ace','G7':'green-seven','G8':'green-eight','G9':'green-nine','G10':'green-ten','GL':'green-lower','GU':'green-upper','GK':'green-king','GA':'green-ace'}
          self.deck=[]

    def create(self):
        self.deck=list(self.card_map)
    
    def shuffle(self):
        return (shuffle(self.deck))
    
    def draw(self):
        return self.deck.pop()
    
    def is_empty(self):
        if (len(self.deck))==0:
            return True
        else:
            return False
        
    def get_deck(self):
        return self.deck

class Player():
    def __init__(self):
   
        self.cards_on_table=[]
        self.collected_cards=[]
        self.hand=[]
        self.score=0
        
    def draw(self):
        # draw a new card from the deck
        self.hand.append(deck.get_deck().pop())

    def is_hand_empty(self):
         if(len(self.hand)==0):
             return True
         else:
             return False
    
    def remove_card(self, card):
        self.hand.remove(card)

    def clear_cards_on_table(self):
        self.cards_on_table.clear()


class User(Player):
    def __init__(self):
        self.name=''
        Player.__init__(self)

    def set_name(self,name):
        self.name=name

    def get_name(self):
        while True:
            user_name=input('What is your first or nick name ?')
            if (len(user_name))>2 and all(char in abc for char in user_name):
                self.set_name(user_name)
                break
            else:
                print('Please enter a valid name with minimum 3 characters!')
    

    def watch(self):
        print(f'\033[1m{user.name}\033[0m has the following cards in \033[1mhand:\033[0m',self.hand)
        for index, card in enumerate(self.hand):
            print_card('H',card,index)

    def select_card(self):
        selected_card=''
        while True:
            selected_card=input("Which card do you select from your hand? (Type '\033[1m--help\033[0m' for help.)").upper()
            if (selected_card in self.hand or selected_card=="--HELP"):
                if (selected_card=='--HELP'):
                    get_rules()
                    continue
                break
            else:
                print('This card is not in your hand!')
        print(f'You, {user.name} have put the following card: ',"\033[1m" + selected_card + "\033[0m")
        self.remove_card(selected_card)
        self.cards_on_table.append(selected_card)

        # display the card that the user put on the table
        # destroy the window in user hand
        windowName='H-'+selected_card
        cv2.destroyWindow(windowName)
        if (len(self.cards_on_table)>0):
            print_card('U',selected_card,len(self.cards_on_table)-1)
        time.sleep(5)
        return selected_card
    
    def pass_card(self):
        while True:
            user_answer=input('Would you like to hit this car? (y/n)')
            if (user_answer in ['y','Y','n','N']):
                break
            else:
                print('Please enter (y)es or (n)o !')
        if (user_answer in ['y','Y']):
            return False
        else:
            show_text('OK, but in this case COMPUTER has picked up the cards!')
            return True
        
    def watch_rules(self):
        while True:
            user_answer=input('Would you like to watch the rules of this game? (y/n)')
            if (user_answer in ['y','Y','n','N']):
                break
            else:
                print('Please enter (y)es or (n)o !')
        if (user_answer in ['y','Y']):
            return True
        else:
            show_text("Yeah ! You already know this game! Are you a Hungarian? Let's start!")
            return False
        
            

class Computer(Player):
    def __init__(self):
        self.seven_cards=[] 
        self.valuable_cards=[]
        self.same_value_cards=[]
        self.other_cards=[]
        Player.__init__(self)

    def show(self):
        # just for testing
        print('Computer hand:',self.hand)
  
    def select_start_card(self):
        card=''
        if(len(self.other_cards)>0):
            card=choice(self.other_cards)
        elif(len(self.valuable_cards)>0):
            card=choice(self.valuable_cards)
        else:
            card=choice(self.seven_cards)
        return card

    def put(self, card):
        print('Computer have just put this card :',"\033[1m" + card + "\033[0m")
        self.remove_card(card)
        self.cards_on_table.append(card)

        # display the card in a window the computer put
        if (len(self.cards_on_table)>0):
            print_card('C',card,len(self.cards_on_table)-1)
        time.sleep(1)
        self.group_cards()
     
    def has_seven_card(self):
        if (len(self.seven_cards)>0):
            return True
        else:
            return False

    def has_valuable_card(self):
        if (len(self.valuable_cards)>0):
            return True
        else:
            return False
        
    def has_same_value_card(self,card):
        value_of_card=card_value(card)
        is_same_value=False
        for element in self.hand:
            if (card_value(element)==value_of_card):
                is_same_value=True
        return is_same_value
            
    def select_same_value_card(self, card):
        value_of_card=card_value(card)
        same_value_card=''
        for element in self.hand:
            if (card_value(element)==value_of_card):
                same_value_card=element
        return same_value_card

    def select_seven_card(self):
        return choice(self.seven_cards)

    def select_low_value_card(self):
        # logic: select a low value card if possible then larger cards
        card=''
        if(len(self.other_cards)>0):
            card=choice(self.other_cards)
        elif(len(self.valuable_cards)>0):
            card=choice(self.valuable_cards)
        else:
            card=choice(self.seven_cards)
        return card

    def group_cards(self):
        self.seven_cards.clear()
        self.valuable_cards.clear()
        self.same_value_cards.clear()
        self.other_cards.clear()

        for card in self.hand:
            value_of_card=card_value(card)
            if value_of_card=='7':
                self.seven_cards.append(card)
            elif value_of_card in ['10','A']:
                self.valuable_cards.append(card)
            else:
                self.other_cards.append(card) 

computer=Computer()
user=User()

def get_rules():
    rules = ["\033[1mINTRODUCTION\033[0m","Zsírozás card game (also known as Zsír - Grease) has a Hungarian origin. This game is closely related to the Czech Sedma (= seven). Although the rules of the game may seem unusual at first, the game itself is easy to learn and the rules allow for specific strategies.","\033[1mPLAYERS\033[0m","You will play with the computer.","\033[1mDECK USED FOR THE GAME\033[0m","The 32-card well known Tell Vilmos deck is used to play this game. This kind of card deck is often used in Central Europe, mainly in Hungary.","\033[1mCOLORS\033[0m","GREEN or Leaves, RED or Hearts, ACORN, PUMPKIN or Bells","\033[1mVALUES\033[0m","lower=2, upper=3, king=4, 7, 8, 9, 10, Ace=11","\033[1mTHE AIM OF THE GAME\033[0m","Aces and tens are called grease, and the object of the game is to get as many of them as possible.","\033[1mDEALING CARDS\033[0m","To start, each player receive 4 cards from the shuffled deck. The remaining deck is face-down on the table and serves as a talon in later rounds.","\033[1mHOW TO PLAY\033[0m","The computer starts the round with a starting card. The next player (now You) can put any card. There is no suit by suit or value by value rule. The last player who puts a card of the same value as the opening card wins the round and pick up the cards. Sevens have a special role. Sevens always take the value of the starting card, so it is a trump card. In a round, there are turns until one of the players picks up the cards. If computer puts a same value or hit card you can hit it as well. In this case computer will ask you about it.","\033[1mPULLING FROM THE TALON\033[0m","At the end of each round, the players (starting with the winner of the round) draw enough cards from the talon to have 4 cards again. If the talon is exhausted, play continues as long as all players have cards in their hands.","\033[1mSCORING\033[0m","If there are no more cards in the talon and in hands the game will end. At the end of the game, the ace and ten cards the players picked up and colleted will be counted. The value of ace is 11, the value of 10 is ten. The winner of the game is who has more points."]

    # Get the current terminal width
    terminal_width = shutil.get_terminal_size().columns

    # Wrap the text to fit the terminal width
    for text in rules:
        wrapped_rules = textwrap.fill(text, width=terminal_width)
        print(wrapped_rules)

    while True:
        print('------------------------------------------')
        user_answer=input("\033[1mPlease type '--resume'\033[0m to continue the game!").upper()
        print('')
        if (user_answer=='--RESUME'):
            break

def card_value(card):
        value_of_card=''
        if (len(card)==2):
            value_of_card=card[-1]
        elif (len(card)==3):
            value_of_card=card[-2:]
        return value_of_card

def show_message(message):
        print(message)

def show_title(title):
        print('-'*(len(title)+4))
        print('|',title,'|')
        print('-'*(len(title)+4))

def show_text(text):
    bold_text = "\033[1m" + text + "\033[0m"
    print('***** ',bold_text,' *****')

def pick_up(player):
    # player pick up the cards from the table and store them in collected cards
    global next_player
    next_player=player
    if (player=='computer'):
        show_text('Oh no! COMPUTER has picked up the cards!')
        computer.collected_cards.extend(computer.cards_on_table+user.cards_on_table)
    else:
        show_text(f'Great! You, {user.name} have picked up  the cards!')
        user.collected_cards.extend(computer.cards_on_table+user.cards_on_table)
    computer.clear_cards_on_table()
    user.clear_cards_on_table()
 
def load_hands():
    # deal the cards / max. 4 cards acceptable in hand of a player
    while True:
        if (len(user.hand)<4 and deck.is_empty()==False):
            computer.draw()
            user.draw()
        else:
            break

def scores():
    computer.score=0
    user.score=0
    for card in computer.collected_cards:
        if (card_value(card)=='10'):
            computer.score+=10
        elif (card_value(card)=='A'):
            computer.score+=11 

    for card in user.collected_cards:
        if (card_value(card)=='10'):
            user.score+=10
        elif (card_value(card)=='A'):
            user.score+=11
    print('SCORES - computer :',"\033[1m" + str(computer.score) + "\033[0m",f' - {user.name} :',"\033[1m" + str(user.score) + "\033[0m")


# Start game
show_title('HUNGARIAN CARD GAME - ZSÍROZÁS')
deck=Deck()
deck.create()
deck.shuffle()
next_player='computer'
round=1

if (user.watch_rules()==True):
    get_rules()

user.get_name()

# Rounds
while True:
    # Round start
    round_start=True
    cv2.destroyAllWindows()
    is_end_of_game=False
    if (deck.is_empty()==True and user.is_hand_empty())==True:
        is_end_of_game=True
        break
    load_hands()
    computer.group_cards()
    show_title('Round '+str(round))

    if (next_player=='computer'):
        show_text('COMPUTER is STARTING the round')
        start_computer_card=computer.select_start_card()
        computer_card=start_computer_card

        computer.put(computer_card)

        while True:
            user.watch()
            user_card=user.select_card()
            if (deck.is_empty()==True and user.is_hand_empty())==True:
                is_end_of_game=True
                if (card_value(user_card)==card_value(computer_card) or user_card in seven_cards):
                    pick_up('user')
                else:
                    pick_up('computer')
                break

            # COMPUTER card logic
            # as default the next computer card has low value, but depending on the user card it may change
            next_computer_card=computer.select_low_value_card()

            if (card_value(user_card)==card_value(start_computer_card)):
                if(user.is_hand_empty()==False):
                    if (computer_card in valuable_cards):
                        # computer want to hit in order to get a valuable card
                        if (computer.has_same_value_card(user_card)):
                            next_computer_card=computer.select_same_value_card(user_card)
                        elif (computer.has_seven_card()):
                            next_computer_card=computer.select_seven_card()
                        computer_card=next_computer_card
                        computer.put(next_computer_card)

                        continue
                    if (computer_card in seven_cards):
                        # user want to hit because of some reason so computer check the reason
                        if (start_computer_card in valuable_cards):
                            # computer want to hit because the start card is valuable
                            if (computer.has_same_value_card(user_card)):
                                next_computer_card=computer.select_same_value_card(user_card)
                            elif (computer.has_seven_card()):
                                next_computer_card=computer.select_seven_card()
                        computer_card=next_computer_card
                        computer.put(next_computer_card)
                        continue
                    if (computer.has_same_value_card(user_card)):
                        # computer want to hit in order to get the next first call
                        next_computer_card=computer.select_same_value_card(user_card)
                        computer_card=next_computer_card
                        computer.put(next_computer_card)
                    else:
                        # user can take the cards
                        pick_up('user')
                        if (deck.is_empty()==True and user.is_hand_empty())==True:
                            is_end_of_game=True
                        break
            else:
                if (user_card in seven_cards):
                    # in case user want to hit, probably computer should hit, too or user can take the cards
                    if (computer.has_seven_card()):
                        if (start_computer_card in valuable_cards):
                            # computer hit only if user start card is valuable
                            next_computer_card=computer.select_seven_card()
                        else: 
                            pick_up('user')
                            if (deck.is_empty()==True and user.is_hand_empty())==True:
                                is_end_of_game=True
                            break 
                        computer.put(next_computer_card)
                        round_start=False
                        continue
                    else:
                        pick_up('user')
                else:
                    pick_up('computer')
                if (deck.is_empty()==True and user.is_hand_empty())==True:
                    is_end_of_game=True
                break

    else:
        # USER round - user put the first card on the table
        show_text(f'{user.name.upper()} is STARTING the round')
        while True:
            user.watch()
            user_card=user.select_card()
            start_user_card=user.cards_on_table[0]

            if (round_start==False):
                # user can hit only with the same value of the start card, or with a seven card
                if (not card_value(user_card)==card_value(start_user_card)):
                    if (user_card not in seven_cards):
                        # if user put a card but it is not a hit card then he must to take back the last card and computer can the the cards
                        user.hand.append(user.cards_on_table[-1])
                        del user.cards_on_table[-1]
                        pick_up('computer')
                        if (deck.is_empty()==True and user.is_hand_empty()==True and computer.is_hand_empty()==True):
                            is_end_of_game=True
                        break
            
            # COMPUTER card logic
            # as default the next computer card has low value, but depending on the user card it may change
            next_computer_card=computer.select_low_value_card()

            if (computer.has_same_value_card(user_card)==True):
                if (user_card in valuable_cards):
                    # computer should hit the user card if he can
                    if (computer.has_same_value_card(user_card)):
                        next_computer_card=computer.select_same_value_card(user_card)
                    else:
                        if(computer.has_seven_card()):
                            next_computer_card=choice(computer.seven_cards)
                else:
                    if (user_card in seven_cards):
                        if (round_start==False):
                            # user put a 7 card, so if the start card is valuable then computer try to hit
                            if(start_user_card in valuable_cards):
                                print('user_card in seven_cards and start_user_card in valuable_cards',computer.hand)
                                if (computer.has_same_value_card(start_user_card)):
                                    print('computer has same value card')
                                    next_computer_card=computer.select_same_value_card(start_user_card)
                                elif (computer.has_seven_card()):
                                    print('computer has seven card')
                                    next_computer_card=choice(computer.seven_cards)
                        else:
                            # if user put 7 card as start card, computer put a low value card
                            computer.put(next_computer_card)
                            pick_up('user')
                            if (deck.is_empty()==True and user.is_hand_empty() and computer.is_hand_empty())==True:
                                is_end_of_game=True
                            break
                    else:
                        next_computer_card=computer.select_same_value_card(user_card)
                computer.put(next_computer_card)
                round_start=False
                if (user.pass_card()==True):
                    # if computer put the same card, but user does not want to hit it
                    pick_up('computer')
                    if (deck.is_empty()==True and user.is_hand_empty() and computer.is_hand_empty())==True:
                        is_end_of_game=True
                    break
                continue
            else:
                if (user_card in valuable_cards):
                    # if user put a valuable card, computer try to hit it
                    if (computer.has_seven_card()):
                        next_computer_card=computer.select_seven_card()
                computer.put(next_computer_card)
                # if computer selected 7 card randomly then next turn is coming
                if (next_computer_card in seven_cards):
                    if (deck.is_empty()==True and user.is_hand_empty() and computer.is_hand_empty())==True:
                        is_end_of_game=True
                        pick_up('user')
                        break
                    if (user.pass_card()==True):
                        # if user does not want to hit it
                        pick_up('computer')
                        if (deck.is_empty()==True and user.is_hand_empty() and computer.is_hand_empty())==True:
                            is_end_of_game=True
                        break
                    continue
                pick_up('user')
                if (deck.is_empty()==True and user.is_hand_empty() and computer.is_hand_empty())==True:
                    is_end_of_game=True
                break
    scores()
    if (is_end_of_game==True):
        break
    round+=1

# Game over
print('No more cards in the deck!')
print("Cards are in computer's hand:",computer.collected_cards)
print("Cards are in user's hand:",user.collected_cards)

if (computer.score>user.score):
    show_text("I'm sorry but computer has won the game.")
elif (computer.score<user.score):
    show_text('User won the game. Congratulations!')
else:
    print('You have the same points.')
show_title('- GAME OVER -')
show_text('See you next time.')

            








