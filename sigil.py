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
        return '%s %x %x' % (self.name, self.attack, self.health)

    def __repr(self):
        return '%s %x %x' % (self.name, self.attack, self.health)
    
class CardSet:
    # Base class for all groups of cards (full deck, player deck, hand, etc)

    def __init__(self, cards=[]):
        self.cards = cards

    def __str__(self):
        ret = ''
        for c in self.cards:
           ret += str(c)

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
            retSet.cards.append(self.cards[i])
        return retSet 


class PlayerDeck(CardSet):
    # Child class of Cardset to represent the players deck

    def __init__(self, cards):
        self.cards = cards

class Hand(CardSet):
    # Child class of Cardset to represent the players hand

    def __init__(self):
        self.cards = []

class Game:
    lanes = 3
    deck = {}
    playerDeck = {}

    def __init__(self):
        deck = FullDeck()
        playerDeck = deck.draw(6)
        print(playerDeck)

game = Game()

