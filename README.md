# ChessPuzzleGeneration [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](https://www.python.org/)[![licenseMIT](https://img.shields.io/badge/license-MIT-blue)]
> [!NOTE]
> This is an artefact of a bachelor project in Software Development @ the IT University of Copenhagen (2025). <br>
> Project title: **Algorithmic Generation of Chess Puzzles**.

This is a **chess puzzle generator** that outputs some chess puzzle in Forsyth-Edwards Notation (FEN).<br>
It has a basic chess engine for evaluating the board state, and uses a genetic algorithm to configure the pieces.

## Installation

**Requires Python 3.13 or newer.**

Clone the repository and install dependencies:

```bash
git clone https://github.com/ChessicaComposer/ChessPuzzleGeneration/
cd ChessPuzzleGeneration
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
$ python main.py

Welcome to the ChessPuzzleGenerator! Type "help" or "?" to list commands
- Usage: run <Composer | FullBoard> <Ply: int> <Population: int> <Time-limit: int | None> <Generation-limit: int | None> <Evaluation-limit: int | None>
- Example: run composer 5 100 14400 none none
ChessPuzzleGenerator>>
```

<hr>

The `run` command normally requires 6 arguments:

| \# | Arg 'type'       | Accepts |
| -- | --               | -- |
| 1 | Generator         | String (Composer, Fullboard) |
| 2 | Ply size          | Int |
| 3 | Population size   | Int |
| 4 | Time limit in s   | Int, None |
| 5 | Generation limit  | Int, None |
| 6 | Evaluation limit  | Int, None |

<hr>

`run` can also take `help` as an argument:

```bash
ChessPuzzleGenerator>> run help

Insufficient number of arguments.
===================================
Usage: run <generator-type> <ply-size> <population-size> <time-limit or None> <generation-limit or None> <evaluation-limit or None>
More info: run help <type>
```

The `type` refers to the above table's arg 'type'.

<hr>

Each `type` has the following aliases:

| \# | Type             | Alias |
| -- | --               | -- |
| 1 | generator-type    | generator |
| 2 | ply-size          | ply |
| 3 | population-size   | population |
| 4 | time-limit        | time |
| 5 | generation-limit  | generation |
| 6 | evaluation-limit  | evaluation |

Example:

```bash
ChessPuzzleGenerator>> run help generator
Available generator types:
==========================
FullBoard | Composer
FullBoard: Initialises a standard chess board. Randomly moves pieces.
Composer: Initialises a chess board with each king in some random, valid position. Randomly adds pieces.
```

## License

MIT License. See the `LICENSE` file for details.

