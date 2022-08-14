# Squardle Solver

[Squardle](https://fubargames.se/squardle/) is a Wordle-like game with some crosswords puzzle elements. Squardle Solver
takes into account the unique constraints this game adds.

## How to run Squardle Solver

1. Run `cli.py` and choose your board size (3 for daily/freeplay, 5 for weekly)
2. Run the game, open Developer Tools (`F12`) and copy the `smallSquares` variable
3. Paste the json into the console
4. The solver will produce wordlists and letter matrix
5. Repeat steps 2-4 after each guess

![Squardle Solver Running](doc/squardle-solver.gif?raw=true "Squardle Solver Running")

## How Squardle Solver Works

Squardle solver is written in Python. It takes the `smallSquares` variable (which holds the board state) as input and
finds all the possible words by:

1. Applying every green/yellow/red/orange/black/white letter found as constraint to the respected wordlist. Squardle
   adds a unique constraint compared to Wordle - a position-dependent disqualified letters
2. Cross-checking each square with the relevant wordlists for possible letter elimination