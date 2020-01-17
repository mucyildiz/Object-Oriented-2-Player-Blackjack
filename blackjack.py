import random
import sys


class Card:

    def __init__(self, value, suit, hidden=None):

        self.value = value
        self.suit = suit
        self.hidden = hidden

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def __str__(self):

        if self.hidden == True:
            return 'Hidden Card'

        else:
            card = '{} of {}'
            return card.format(self.value, self.suit)

    def __add__(self, card):
        return self.get_value() + card.get_rank()

    def __radd__(self, integer):
        return integer + self.get_rank()


class Deck:

    def __init__(self):

        suits = ['Clubs', 'Diamonds', 'Spades', 'Hearts']
        values = ['Ace', '2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'King', 'Queen', 'Jack']
        self.deck = []
        for suit in suits:
            for i in range(len(values)):
                self.deck.append(Card(values[i], suit))

    def print_deck(self):

        for i in range(len(self.deck)):
            print(str(self.deck[i]))

    def shuffle(self):
        self.deck = random.sample(self.deck, len(self.deck))

    def remove_card(self, card):

        if card in self.deck:
            self.deck.remove(card)
            return self.deck

    def isEmpty(self):
        return len(self.deck) == 0

    def pop_card(self):

        if not Deck.isEmpty(self):
            return self.deck.pop(0)

        else:
            raise Exception("OUT OF CARDS")


class Player:

    def __init__(self, deck, chips, score=None):
        
        self.deck = deck
        self.hand = []
        self.chips = chips
        self.score = self.sum_score()
    
    def has_ace(self): 
        for i in range(len(self.hand)):
            if self.hand[i].value == 'Ace':
                return True
        return False

    def get_rank(self, card):

        # if card.value == 'Ace':
        #     if self.score <= 10:
        #         return 11
        #     if self.score > 10 and self.score < 21:
        #         return 1
                

        if card.value == 'King' or card.value == 'Queen' or card.value == 'Jack':
            return 10

        else:
            return int(card.value)

    def hit(self, hide=None):

        card_at_top = self.deck.pop_card()
        card_at_top.hidden = hide
        self.hand.append(card_at_top)
        return card_at_top

    def print_hand(self):

        for card in self.hand:
            print(card)
        print('\n')

    def sum_score(self):

        sum = 0
        for i in range(len(self.hand)):

            if self.hand[i].value == 'Ace':
                if sum > 10:
                    sum += 1
                if sum <= 10:
                    sum += 11

            else:
                sum += self.get_rank(self.hand[i])
        
        #edge case for when the ace is introduced as the dealers third hit
        if sum > 21 and self.has_ace():
            sum = 0
            for i in range(len(self.hand)):

                if self.hand[i].value == 'Ace':
                    sum += 1
                else:
                    sum += self.get_rank(self.hand[i])

        return sum

    def show_cards(self):

        for card in self.hand:
            if card.hidden == True:
                card.hidden = False
        return self.hand

class BlackJack:

    def __init__(self, player, dealer, deck, bet):

        self.player = player
        self.dealer = dealer
        self.deck = deck
        self.bet = bet

    def start_game(self):

        self.deck.shuffle()  # shuffle the deck
        self.player.hit()  # give player his cards
        self.player.hit()
        self.check_w_or_l(self.bet)
        print('\n' + "The player's hand is: " + '\n')
        self.player.print_hand()

        # give dealer his cards, hide one
        self.dealer.hit()
        self.dealer.hit(hide=True)
        print("The dealer's hand is: " + '\n')
        self.dealer.print_hand()

    def hit_or_stand(self):

        h_or_s = input("Type 'hit' or 'stand' or 'double'." + '\n')

        while h_or_s not in('hit', 'stand', 'double'):
            print("YOU MUST TYPE 'HIT' OR 'STAND' OR 'DOUBLE'.")
            h_or_s = input("Type 'hit' or 'stand' or 'double'." + '\n')

        while h_or_s == 'hit':

            hit_card = self.player.hit()
            print('\n' + "You picked up a " + hit_card.__str__())
            print('\n' + "Your score is " + str(self.player.sum_score()))
            self.check_w_or_l(self.bet)

            print("Your current cards are " + '\n')
            self.player.print_hand()
            print("Your current score is " +
                  str(self.player.sum_score()) + '\n')

            h_or_s = input("Type 'hit' or 'stand'" + '\n')
        
        if h_or_s == 'double':

            if self.bet * 2 > self.player.chips.dollars:
                while h_or_s == 'double':
                    print('\n' + "You don't have enough money to double down.")
                    h_or_s = input("Type 'hit' or 'stand'." + '\n')

            hit_card = self.player.hit()
            print('\n' + "You picked up a " + hit_card.__str__())
            print('\n' + "Your score is " + str(self.player.sum_score()))
            self.dealer_turn(self.bet * 2)
    


        if h_or_s == 'stand':
            self.dealer_turn()
        

    def loss(self, bet):

        print("Your hand was: " + '\n')
        self.player.print_hand()
        print("You had a score of: " + str(self.player.sum_score()) + '\n')


        print("The dealer's hand was: " + '\n')
        self.dealer.show_cards()
        self.dealer.print_hand()
        print("The dealer had a score of: " + str(self.dealer.sum_score()) + '\n')

        self.player.chips.lost_bet(bet)

        q = input(
            "You lost. Would you like to play again? Type 'yes' or 'no'." + '\n')
        while q not in ('yes', 'no'):
            print("YOU MUST TYPE IN 'YES' OR 'NO'.")
            q = input(
            "You lost. Would you like to play again? Type 'yes' or 'no'." + '\n')
        if q.lower() == 'yes':
            print("___________________________________________________________")
            main(self.player.chips.dollars)
        else:
            sys.exit()

    # made two different functions for win or loss because it's easier and more clear to just call win() or loss()
    def win(self, bet):

        if self.player.sum_score() == 21:
            print('\n' + "________________BLACKJACK________________" + '\n')
            self.player.chips.won_bet(self.bet * 1.5)        

        else:
            print("Your hand was: " + '\n')
            self.player.print_hand()
            print('\n' + "You had a score of: " + str(self.player.sum_score()) + '\n')

            print("The dealer's hand was: " + '\n')
            self.dealer.show_cards()
            self.dealer.print_hand()
            print('\n' + 'The dealer had a score of: ' + str(self.dealer.sum_score()) + '\n')

            self.player.chips.won_bet(self.bet)        

        q = input(
            "You won. Would you like to play again? Type 'yes' or 'no'." + '\n')
        while q not in ('yes', 'no'):
            print("YOU MUST TYPE IN 'YES' OR 'NO'.")
            q = input(
            "You won. Would you like to play again? Type 'yes' or 'no'." + '\n')

        if q.lower() == 'yes':
            print("___________________________________________________________")
            main(self.player.chips.dollars)
        else:
            sys.exit()

    def check_w_or_l(self, bet):

        if self.player.sum_score() > 21:
            self.loss(bet)

        if self.player.sum_score() == 21:
            self.win(bet)

    def dealer_turn(self, bet=None):

        print('\n' + "Dealer's turn, dealer's hand is:" + '\n')
        self.dealer.show_cards()
        self.dealer.print_hand()

        while self.dealer.sum_score() < 17:
            dealer_hit = self.dealer.hit()
            print("Dealer hit and got " + dealer_hit.__str__() + '\n')

        dealer_score = self.dealer.sum_score()
        player_score = self.player.sum_score()

        if dealer_score == 21 and not player_score == 21:
            if bet == None:
                self.loss(self.bet)
            else:
                self.loss(bet)

        if dealer_score > 21 and player_score > 21:
            if bet == None:
                self.loss(self.bet)
            else:
                self.loss(bet)

        if dealer_score > 21 and player_score <= 21:
            if bet == None:
                self.win(self.bet)
            else:
                self.win(bet)

        if dealer_score < player_score:
            if bet == None:
                self.win(self.bet)
            else:
                self.win(bet)

        if dealer_score > player_score:
            if bet == None:
                self.loss(self.bet)
            else:
                self.loss(bet)

        else:
            print("It's a tie. Start again." + '\n')
            print("___________________________________________________________")
            main(self.player.chips.dollars)

class Chips:

    def __init__(self, worth, color, dollars):
        self.worth = worth
        self.color = color
        self.dollars = dollars
        self.count = self.dollars_to_chips()
    
    def dollars_to_chips(self, dollars=None):
        if dollars == None:
            dollars = self.dollars
        chips = []

        for i in range(0, len(self.worth)): 
            chip_count = dollars // self.worth[i]
            chips.append(chip_count)
            dollars = dollars % self.worth[i]

        return chips
    
    # will use this method for when the user wins or loses a bet and we want to see how much money he has left
    def chips_to_dollars(self):

        dollar_amounts = []
        for i in range(len(self.count)):
            dollar_amounts.append(self.count[i] * self.worth[i])
        
        dollars = 0
        for i in range(len(dollar_amounts)):
            dollars += dollar_amounts[i]

        return dollars

    def get_chips(self):

        players_chips = ''
        sing_pl = ['chip', 'chips']
        for_format = 'You have {} {} {}. '

        for i in range(len(self.count)):
            if self.count[i] > 1 or self.count[i] == 0:
                players_chips += for_format.format(str(self.count[i]), self.color[i].lower(), sing_pl[1])
            else:
                players_chips += for_format.format(str(self.count[i]), self.color[i].lower(), sing_pl[0])

        dollar_amount = self.chips_to_dollars()
        players_chips += 'This equates to ' + '${:,.2f}'.format(dollar_amount) 

        return players_chips
    
    def lost_bet(self, bet):
        self.dollars -= bet
        self.count = self.dollars_to_chips()
        print(self.get_chips())
    
    def won_bet(self, bet):
        self.dollars += bet
        self.count = self.dollars_to_chips()
        print(self.get_chips())

        

    def __add__(self, coin):
        return self.worth + coin.worth
    
    def chip_count(self, coin):
        return self.count + coin.count




def main(money):

    if money == 0:
        print("Looks like you ran out of money. It's time to stop!")
        sys.exit()

    worth = (1000, 500, 100, 25, 5, 1)
    color = ('Orange', 'Purple', 'Black', 'Green', 'Red', 'White')

    player_chips = Chips(worth, color, money)
    dealer_chips = Chips(worth, color , 0)

    deck = Deck()
    user = Player(deck, player_chips)
    dealer = Player(deck, dealer_chips)

    bet = int(input("How much do you want to bet?"))

    while(bet > money):
        print("You don't have enough money to bet that much.")
        bet = int(input("How much do you want to bet?"))

    blackjack = BlackJack(user, dealer, deck, int(bet))
    blackjack.start_game()
    blackjack.hit_or_stand()

money = int(input("How much money did you come with?"))
main(money)



