import random

class Card:
    # Class to represent a card

    def __init__(self, name, short, attack, health, cost, sigils):
        self.name = name
        self.short = short
        self.attack = attack
        self.health = health
        self.cost = cost
        self.sigils = sigils

    def __str__(self):
        return self.log()

    def __repr(self):
        return self.log()
    
    def log(self):
        #return '<Card: %s a:%x h:%x>' % (self.name, self.attack, self.health)
        return '<Card:%s>' % (self.name)

    def shortLog(self):
        return '[%s]' % (self.short)



class CardSet:
    # Base class for all groups of cards (full deck, player deck, hand, etc)

    def __init__(self, cards=[]):
        self.cards = cards

    def __str__(self):
        return self.log()

    def __repr(self):
        return self.log()
    
    def log(self):
        ret = ''
        for c in self.cards:
            ret += str(c)
        return "[%s]" % ret

class FullDeck(CardSet):
    # Child Class of Cardset to represent the full deck of available cards
    
    def __init__(self, cards=[]):
        self.cards = cards
        self.cards.append( Card("Squirrel", "SQ", 0, 1, 0, []) )
        self.cards.append( Card("Wolf", "WF", 2, 3, 2, []) )
        self.cards.append( Card("Sparrow", "SP", 0, 1, 0, []) )
        self.cards.append( Card("Deer", "DR", 1, 1, 1, []) )

    def draw(self, n):
        retSet = CardSet([]);
        for x in range(n):
            i = random.randrange(0, len(self.cards))
            print("drawing random card: %s" % self.cards[i])
            retSet.cards.append(self.cards[i])
        return retSet 


class PlayerDeck(CardSet):
    # Child class of Cardset to represent the players deck

    def __init__(self, cards): 
        self.cards = cards

    def draw(self, n):
        # draw hand from the player's deck take top n
        retSet = CardSet(self.cards[:n]);
        # remove those cards from player deck
        self.cards = self.cards[n:]
        return retSet 


class Hand(CardSet):
    # Child class of Cardset to represent the players hand

    def __init__(self):
        self.cards = []

class Field():
    # Class to represent the field where cards are played
    lanes = 4
    preplay = [None] * lanes
    p1 = [None] * lanes
    p2 = [None] * lanes
    field = [preplay, p1, p2]

    def __init__(self):
        pass

    def play(self, player, card, lane):
        if self.field[player][lane] is not None:
            raise InputError('Not an open space')
        else: 
            self.field[player][lane] = card
        return
            
    def log(self):
        ret = ''
        for f in self.field:
            for c in f:
                if c is None:
                    ret += ' [  ]'
                else:
                    ret += ' ' + c.shortLog()
            ret += '\n'
        return "%s" % ret

    def __str__(self):
        return self.log()

    def __repr(self):
        return self.log()


# states
class STATE:
    NEW = 1
    PICK = 2
    PLACE = 3
    ATTACK = 4
    GAMEOVER = 5

class EVENT:
    PICK_CARD = 1
    PICK_LANE = 2
    BELL = 3
    QUIT = 4

class InputError(Exception):
    def __init__(self, data):
        self.data = data
    def __str__(self):
        return repr(self.data)

class Game():

    lanes = 4
    deck = {}

    def __init__(self):
        # initialize a new Deck
        deck = FullDeck()
        # initialize a playing surface
        self.field = Field()
        # Draw 6 random cards from deck to make a player deck
        self.playerDeck = PlayerDeck(deck.draw(6).cards)
        # Draw 3 cards from player deck to make a player hand
        self.hand = self.playerDeck.draw(3);
        # set the state to new
        self.state = STATE.PICK
        self.selectedCard = None
        
    def event(self, e, i=None):
        if e == EVENT.QUIT:
            self.state = STATE.GAMEOVER
        if self.state == STATE.ATTACK:
            self.state = STATE.GAMEOVER
        if self.state == STATE.PICK:
            if e == EVENT.PICK_CARD:
                try:
                    self.selectedCard = self.hand.cards.pop(i)
                    self.state = STATE.PLACE
                except:
                    raise InputError("Not a valid card")
            if e == EVENT.BELL:
                self.state = STATE.ATTACK
        elif self.state == STATE.PLACE:
            if e == EVENT.PICK_LANE:
                try:
                    self.field.play(2, self.selectedCard, i)
                    self.selectedCard = None
                    self.state = STATE.PICK
                except:
                    raise InputError("Not a valid lane")


class Test:

    def __init__(self):
        # initialize a new Game
        self.game = Game()

        # GAME LOOP
        while not self.game.state == STATE.GAMEOVER:

            print()
            print(self.game.field)
            print()
            print(self.game.hand)
            print()
            
            match self.game.state:
                case STATE.PICK:
                    while True:
                        inp = input("Select a card (1-3) or (b) for bell:")
                        if inp == 'b':
                            self.game.event(EVENT.BELL)
                            break
                        try:
                            self.game.event(EVENT.PICK_CARD, int(inp) - 1)
                        except:
                            print("Invalid Input")
                            continue
                        break
                    while True and self.game.state == STATE.PLACE:
                        inp = input("Select a position to play(1-4):")
                        try:
                            self.game.event(EVENT.PICK_LANE, int(inp) - 1)
                        except:
                            print("Invalid Input")
                            continue
                        break
                case STATE.ATTACK:
                    print("Attack!!")
                    print("you lose")
                    self.game.event(EVENT.QUIT)

def main():
    test = Test()

if __name__ == '__main__':
    main()



