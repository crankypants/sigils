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
    lanes = 3
    preplay = [None, None, None]
    p1 = [None, None, None]
    p2 = [None, None, None]
    field = [preplay, p1, p2]

    def __init__(self):
        pass

    def play(self, player, card, lane):
        if self.field[player][lane] is not None:
            print('Not an open space')
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


class Test:
    lanes = 3
    deck = {}
    playerDeck = {}
    hand = {}
    field = {}

    def __init__(self):
        # initialize a new Deck
        self.deck = FullDeck()

        # initialize a playing surface
        self.field = Field()
        print()
        print("Full Deck: %s" % self.deck)
        print()

        # Draw 6 random cards from deck to make a player deck
        self.playerDeck = PlayerDeck(self.deck.draw(6).cards)
        print("Player Deck: %s" % self.playerDeck)
        print()

        # Draw 3 cards from player deck to make a player hand
        print("now drawing a hand of 3")
        self.hand = self.playerDeck.draw(3);
        print("hand: %s" % self.hand)
        print()

        # validate they cards are removed from the player deck
        print("Player Deck: %s" % self.playerDeck)
        print()

        # show the state of the empty field
        print('Field:')
        print(self.field)
        print()

        # Player puts a card on the field
        print('Player plays first card to first lane')
        self.field.play(2, self.hand.cards.pop(0), 0)
        print(self.field)
        print()

        # validate the card is removed from the hand
        print("hand: %s" % self.hand)

def main():
    test = Test()

if __name__ == '__main__':
    main()



