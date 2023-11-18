import unittest
from harness import *

class Test(unittest.TestCase):
    # hand_rank() tests
    def test_royal_flush(self):
        hand = [('Ace', 'Hearts'), ('King', 'Hearts'), ('Queen', 'Hearts'), ('Jack', 'Hearts'), ('10', 'Hearts')]
        self.assertEqual(hand_rank(hand), (10, hand), "Should be a Royal Flush")

    def test_straight_flush(self):
        hand = [('9', 'Clubs'), ('8', 'Clubs'), ('7', 'Clubs'), ('6', 'Clubs'), ('5', 'Clubs')]
        self.assertEqual(hand_rank(hand), (9, hand), "Should be a Straight Flush")

    def test_four_of_a_kind(self):
        hand = [('9', 'Hearts'), ('9', 'Clubs'), ('9', 'Diamonds'), ('9', 'Spades'), ('5', 'Hearts')]
        self.assertEqual(hand_rank(hand), (8, hand), "Should be Four of a Kind")

    def test_full_house(self):
        hand = [('10', 'Hearts'), ('10', 'Clubs'), ('10', 'Diamonds'), ('8', 'Spades'), ('8', 'Hearts')]
        self.assertEqual(hand_rank(hand), (7, hand), "Should be a Full House")

    def test_flush(self):
        hand = [('Ace', 'Spades'), ('10', 'Spades'), ('7', 'Spades'), ('6', 'Spades'), ('3', 'Spades')]
        self.assertEqual(hand_rank(hand), (6, hand), "Should be a Flush")

    def test_straight(self):
        hand = [('6', 'Hearts'), ('5', 'Clubs'), ('4', 'Diamonds'), ('3', 'Spades'), ('2', 'Hearts')]
        self.assertEqual(hand_rank(hand), (5, hand), "Should be a Straight")

    def test_three_of_a_kind(self):
        hand = [('Queen', 'Hearts'), ('Queen', 'Clubs'), ('Queen', 'Diamonds'), ('8', 'Spades'), ('4', 'Hearts')]
        self.assertEqual(hand_rank(hand), (4, hand), "Should be Three of a Kind")

    def test_two_pair(self):
        hand = [('Jack', 'Hearts'), ('Jack', 'Clubs'), ('3', 'Diamonds'), ('3', 'Spades'), ('2', 'Hearts')]
        self.assertEqual(hand_rank(hand), (3, hand), "Should be Two Pair")

    def test_one_pair(self):
        hand = [('10', 'Hearts'), ('10', 'Clubs'), ('Ace', 'Diamonds'), ('8', 'Spades'), ('7', 'Hearts')]
        self.assertEqual(hand_rank(hand), (2, hand), "Should be One Pair")

    def test_high_card(self):
        hand = [('King', 'Hearts'), ('Queen', 'Clubs'), ('Jack', 'Diamonds'), ('9', 'Spades'), ('7', 'Hearts')]
        self.assertEqual(hand_rank(hand), (1, hand), "Should be High Card")

    # preflop_hand_rank() tests
    def test_pair_aces(self):
        hand = [('Ace', 'Hearts'), ('Ace', 'Spades')]
        self.assertEqual(preflop_hand_rank(hand), (1, hand), "Should be a Pair of Aces")

    def test_pair_kings(self):
        hand = [('King', 'Hearts'), ('King', 'Spades')]
        self.assertEqual(preflop_hand_rank(hand), (1, hand), "Should be a Pair of Kings")

    def test_pair_twos(self):
        hand = [('2', 'Clubs'), ('2', 'Diamonds')]
        self.assertEqual(preflop_hand_rank(hand), (1, hand), "Should be a Pair of Twos")

    def test_high_card_ace_king(self):
        hand = [('Ace', 'Hearts'), ('King', 'Spades')]
        self.assertEqual(preflop_hand_rank(hand), (0, hand), "Should be Ace High")

    def test_high_card_queen_jack(self):
        hand = [('Queen', 'Hearts'), ('Jack', 'Spades')]
        self.assertEqual(preflop_hand_rank(hand), (0, hand), "Should be Queen High")

    def test_high_card_ten_nine(self):
        hand = [('10', 'Hearts'), ('9', 'Spades')]
        self.assertEqual(preflop_hand_rank(hand), (0, hand), "Should be 10 High")

    def test_high_card_mixed(self):
        hand = [('8', 'Clubs'), ('4', 'Diamonds')]
        sorted_hand = sorted(hand, key=lambda x: x[0], reverse=True)
        self.assertEqual(preflop_hand_rank(hand), (0, sorted_hand), "Should be 8 High")

    def test_high_card_low(self):
        hand = [('3', 'Hearts'), ('2', 'Spades')]
        self.assertEqual(preflop_hand_rank(hand), (0, hand), "Should be 3 High")

    # Functionality Testing
    # Testing if blinds are correctly posted and deducted from player chips.
    def test_blinds_posted(self):
        players = [Player("Alpha"), Player("Bravo")]
        deck = Deck()
        pot = Pot()
        blind = 20  # Big blind
        dealer_position = 0
        preflop(players, dealer_position, deck, pot, blind)

        expected_alpha_chips = 2000 - blind // 2  # Small blind is half of the big blind
        self.assertEqual(players[0].chips, expected_alpha_chips)

        expected_bravo_chips = 2000 - blind  # Big blind
        self.assertEqual(players[1].chips, expected_bravo_chips)


if __name__ == '__main__':
    unittest.main()
