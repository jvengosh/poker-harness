class Player:
    def __init__(self, n, strategy=None, chips=2000):
        """
        Initialize a Player object.

        Args:
            n (str): The name of the player.
            strategy (Strategy, optional): The player's strategy for decision-making (default is None).
            chips (int, optional): The initial number of chips the player has (default is 2000).
        """
        self.name = n
        self.chips = chips
        self.action = ""  # The player's chosen action in the current round
        self.fold = False  # Flag indicating whether the player has folded
        self.round_bet = 0  # The amount of chips the player has bet in the current round
        self.cards = []  # The player's hole cards
        self.strategy = strategy  # The strategy used by the player for decision-making

    def reset(self):
        """
        Reset the player's round-specific attributes to their initial state.
        """
        self.action = ""
        self.fold = False
        self.round_bet = 0
        self.cards = []

    def choose_action(self, community_cards, min_bet):
        """
        Choose an action for the player based on their strategy and the current game state.

        Args:
            community_cards (list of tuple): The community cards that are visible to all players.
            min_bet (int): The minimum bet amount for the current round.

        Returns:
            str: The chosen action for the player (e.g., "fold," "call," "raise," or "all-in").
        """
        action = self.strategy.decide_action(self, community_cards, min_bet)
        self.action = action
        return action
