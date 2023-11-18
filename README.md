# SCAI Poker Jam

Welcome to Poker Jam! This competition is designed to simulate a simplified version of a poker game, allowing you to come up with unique strategies, build your own custom algorithms, and play poker against other strategies!

## Getting Started

To get started with this poker game project, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   $ git clone https://github.com/jvengosh/poker-harness
   ````
   ```bash
   $ cd poker-harness
   ```
2. Ensure you have Python installed on your machine.
3. Run the game by executing the following command:
    ```bash
   $ python game.py
   
   OR 
   
   $ python3 game.py
   ```
4. At base level, the game will play one hand and display the hand winner, current chip amounts, etc.
5. Start building your own strategy! Further instructions will be provided to you during the competition.

## Project Structure
Here's a brief overview of the project's file structure:

- `game.py`: The entry point for running the game. You can specify the number of rounds and create player objects here. This can be used for testing and will also be used to simulate matches during the competition.

- `harness.py`: Contains utility classes and functions for managing pots, decks, blinds, hand ranking, and more. **DO NOT** change anything here unless explicitly told to do so.

- `player.py`: Defines the `Player` class, which represents a player in the game. Players can have different strategies for decision-making, showcased in the `game.py` file.

- `strategy.py`: Contains the strategy classes that players can use for making betting decisions. **This will be your home base to develop strategies, code, etc.**


## Important Notes
- **Players with Insufficient Chips**: In this simplified version of poker, players who cannot meet the big blind requirement during the preflop are considered out of the game for that round. They will not participate in that particular hand.

- **Customizing the Game**: You can customize the game by adjusting the number of rounds, player strategies, or other game parameters in the `game.py` file.

- **Player Strategies**: Players can have different strategies for decision-making. You can create your own custom strategies by defining new classes in the `strategy.py` file.


### Have fun playing poker! 🃏🎉
