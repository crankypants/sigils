import random

class Card:
    # Class to represent a card

    def __init__(self, name, attack, health, cost, sigils):
        self.name = name
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
        return '<Card: %s>' % (self.name)

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
        self.cards.append( Card("Squirrel", 0, 1, 0, []) )
        self.cards.append( Card("Wolf", 2, 3, 2, []) )
        self.cards.append( Card("Sparrow", 0, 1, 0, []) )
        self.cards.append( Card("Deer", 1, 1, 1, []) )

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

class Game:
    lanes = 3
    deck = {}
    playerDeck = {}
    hand = {}

    def __init__(self):
        deck = FullDeck()
        print()
        print("Full Deck: %s" % deck)
        print()
        playerDeck = PlayerDeck(deck.draw(6).cards)
        print("Player Deck: %s" % playerDeck)
        print()
        print("now drawing a hand of 3")
        hand = playerDeck.draw(3);
        print("hand: %s" % hand)
        print()
        print("Player Deck: %s" % playerDeck)
        print()


game = Game()

