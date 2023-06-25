from typing import Any
import numpy as np
import math
import random

class Player():
    def __init__(self, n):
        self.name = n
        self.chips = 2000
        self.action = ""
        self.round_bet = 0
        self.cards = []

    def choose_action(self):
        self.action = random.choice(["fold", "call", "raise", "all-in"])
        if (self.action == "raise"):
            return #bet
        return 0

class Pot():
    def __init__(self):
        self.chips = 0
        self.cards = []

    def reset(self):
        self.chips = 0
        self.cards = []

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

        self.cards = [(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return ', '.join([f'{rank} of {suit}' for rank, suit in self.cards])


# blinds: calculated the blinds for the round and deducts the total from each player
# parameters:
#       big: player who is responsible for big blind
#       little: player who is responsible for little blind
#       blind: size of big blind
# returns: total added to the pot
#
# TODO: Handle all-in on blind

def blinds(big, little, blind):
    big.chips -= blind
    big.round_bet = blind
    little.chips -= math.floor(blind / 2)
    little.round_bet = math.floor(blind / 2)
    return math.floor(1.5 * blind)

# preflop: handles the logic for the preflop
# parameters:
#       players: list of players active in the round
# returns: players remaining in play

def preflop(players, dealer, deck, pot):
    # Blinds
    little = players[(dealer + 1) % len(players)] # little is left of dealer
    big = players[(dealer + 2) % len(players)] # big is left of little

    pot.chips += blinds(big, little, blind)
    # print(pot.chips)

    # Reorder player list with dealer at back
    print("Dealer: ", players[dealer].name + ", Little: ", little.name + ", Big: ", big.name)
    players = players[(dealer + 1):] + players[:(dealer + 1)]
    print(players[0].name)

    # Deal Cards
    for i in range(2):
        for p in players:
            p.cards.append(deck.draw())

    # Betting Loop
    # TODO: implement betting interactions
    min_bet = blind
    raise_count = 0

    while(True):
        for player in players:
            player.choose_action() # remove (used for limited testing)
            if (player.action == "fold"):
                print("fold")
                return players
            elif (player.action == "call"):
                if (player.chips < min_bet - player.round_bet):
                    print("all-in")
                else:
                    print("call")
            elif (player.action == "raise"):
                if (raise_count == 3):
                    print("call")
                else:
                    raise_count += 1
                    print("raise")
            elif (player.action == "all-in"):
                player.round_bet += player.chips
                player.chips = 0
            else:
                print("No Action")

    return players

def main():
    player_0 = Player("Alpha")
    player_1 = Player("Bravo")
    player_2 = Player("Charlie")
    player_3 = Player("Delta")

    pot = Pot()

    deck = Deck()
    deck.shuffle()

    global blind
    blind = 20

    players = [player_0, player_1, player_2, player_3]
    dealer = math.floor(random.random() * 4)

    preflop(players, dealer, deck, pot)

    print(player_0.cards, player_0.chips)

    return

main()