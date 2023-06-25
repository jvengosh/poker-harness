import numpy as np
import math
import random
from itertools import combinations

class Player():
    def __init__(self, n):
        self.name = n
        self.chips = 2000
        self.action = ""
        self.fold = False
        self.round_bet = 0
        self.cards = []

    def reset(self):
        self.action = ""
        self.fold = False
        self.round_bet = 0
        self.cards = []

    def choose_action(self, community):
        cards = self.cards
        if (len(community) != 0):
            cards.append(community)
            all_hands = list(combinations(cards, 5))
            best_hand = max(all_hands, key=hand_rank)
        else:
            best_hand = preflop_hand_rank(cards)
        print(best_hand)
        return

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

# hand_rank: returns the strength of the poker hand
# parameters:
#       hand: the hand to be evaluated
# returns: a tuple with the strength of the hand and the hand sorted

def hand_rank(hand):
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']

    # Count the occurrences of each rank and suit in the hand
    rank_count = {}
    suit_count = {}
    for card in hand:
        rank, suit = card
        rank_count[rank] = rank_count.get(rank, 0) + 1
        suit_count[suit] = suit_count.get(suit, 0) + 1

    # Check for different hand ranks in decreasing order of strength
    # Return a tuple with the rank of the hand and the relevant cards for tie-breakers

    # Royal Flush: A, K, Q, J, 10 of the same suit
    if all(suit_count[suit] == 5 for suit in suits) and all(rank_count[rank] == 1 for rank in ranks[-5:]):
        return (10, hand)

    # Straight Flush: Five consecutive cards of the same suit
    for suit in suits:
        if suit_count[suit] == 5:
            suited_cards = [card for card in hand if card[1] == suit]
            suited_ranks = [ranks.index(card[0]) for card in suited_cards]
            suited_ranks.sort()
            if max(suited_ranks) - min(suited_ranks) == 4:
                return (9, suited_cards)

    # Four of a Kind: Four cards of the same rank
    for rank, count in rank_count.items():
        if count == 4:
            quads_cards = [card for card in hand if card[0] == rank]
            return (8, quads_cards)

    # Full House: Three of a kind and a pair
    has_three = False
    has_pair = False
    three_rank = ''
    pair_rank = ''
    for rank, count in rank_count.items():
        if count == 3:
            has_three = True
            three_rank = rank
        elif count == 2:
            has_pair = True
            pair_rank = rank
    if has_three and has_pair:
        three_cards = [card for card in hand if card[0] == three_rank]
        pair_cards = [card for card in hand if card[0] == pair_rank]
        return (7, three_cards + pair_cards)

    # Flush: Five cards of the same suit
    for suit in suits:
        if suit_count[suit] == 5:
            suited_cards = [card for card in hand if card[1] == suit]
            return (6, suited_cards)

    # Straight: Five consecutive cards of any suit
    ranks_in_hand = [ranks.index(card[0]) for card in hand]
    ranks_in_hand.sort()
    if max(ranks_in_hand) - min(ranks_in_hand) == 4 and len(set(ranks_in_hand)) == 5:
        return (5, hand)

    # Three of a Kind: Three cards of the same rank
    for rank, count in rank_count.items():
        if count == 3:
            trips_cards = [card for card in hand if card[0] == rank]
            return (4, trips_cards)

    # Two Pair: Two pairs of cards
    pair_ranks = []
    for rank, count in rank_count.items():
        if count == 2:
            pair_ranks.append(rank)
    if len(pair_ranks) >= 2:
        pair_ranks.sort(key=lambda x: ranks.index(x), reverse=True)
        pair1_cards = [card for card in hand if card[0] == pair_ranks[0]]
        pair2_cards = [card for card in hand if card[0] == pair_ranks[1]]
        return (3, pair1_cards + pair2_cards)

    # One Pair: Two cards of the same rank
    for rank, count in rank_count.items():
        if count == 2:
            pair_cards = [card for card in hand if card[0] == rank]
            return (2, pair_cards)

    # High Card: No matching ranks or suits
    sorted_hand = sorted(hand, key=lambda x: (ranks.index(x[0]), suits.index(x[1])), reverse=True)
    return (1, sorted_hand)

# preflop_hand_rank: returns the strength of the hole cards
# parameters:
#       handL the hand to be evaluated
# returns: a tuple with the strength of the hand and the hand sorted

def preflop_hand_rank(hand):
    ranks = ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']

    # Count the occurrences of each rank and suit in the hand
    rank_count = {}
    suit_count = {}
    for card in hand:
        rank, suit = card
        rank_count[rank] = rank_count.get(rank, 0) + 1
        suit_count[suit] = suit_count.get(suit, 0) + 1

    # Check for different hand ranks in decreasing order of strength
    # Return a tuple with the rank of the hand and the relevant cards for tie-breakers

    # Pocket Pair: Two cards of the same rank
    for rank, count in rank_count.items():
        if count == 2:
            pair_cards = [card for card in hand if card[0] == rank]
            return (1, pair_cards)

    # High Cards: No matching ranks or suits
    sorted_hand = sorted(hand, key=lambda x: (ranks.index(x[0]), suits.index(x[1])), reverse=True)
    return (0, sorted_hand)

# preflop: handles the logic for the preflop
# parameters:
#       players: list of players active in the round
# returns: players remaining in play

def preflop(players, dealer, deck, pot):
    # Blinds
    little = players[(dealer + 1) % len(players)]   # little is left of dealer
    big = players[(dealer + 2) % len(players)]      # big is left of little

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
            player.choose_action(pot.cards) # remove (used for limited testing)
            if (player.fold == False):
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
                    return

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