import time

import cli_ui

from common.conditions import Conditions
from genetic import FullBoard, Composer
from genetic.utility import chess_int_to_board


class Main(cli_ui):

    # Choices
    _generators = ["FullBoard", "Composer"]
    chosen_generator = cli_ui.ask_choice("Choose a generator", choices=_generators, sort=False)

    _ply = ["5", "7", "9"] # For Composer; default FullBoard's _ply to 5.
    chosen_ply = int(cli_ui.ask_choice("Choose ply", choices=_ply, sort=False))

    chosen_population = int(cli_ui.ask_string("Choose population size"))

    chosen_time_limit = int(cli_ui.ask_string("Choose time-limit in seconds"))

    chosen_generation_limit = int(cli_ui.ask_string("Choose generation-limit"))

    chosen_evaluation_limit = int(cli_ui.ask_string("Choose evaluation-limit"))

    # Running

    cli_ui.info_section("Welcome to ChessPuzzleGeneration.")

    time_: float
    conditions = Conditions(chosen_time_limit, chosen_generation_limit, chosen_evaluation_limit)
    result = []

    if chosen_generator is _generators[0]:
        start_time = time.time()
        result = FullBoard(chosen_ply).run(chosen_population, conditions)
        time_ = time.time() - start_time
    elif chosen_generator is _generators[1]:
        start_time = time.time()
        result = Composer(chosen_ply).run(chosen_population, conditions)
        time_ = time.time() - start_time
    else: raise ValueError

    for res in result:
        board = chess_int_to_board(c.body)
        print(board.fen())

    print("\n==========================\n",
          "Generator: ", _generators,
          " | Ply: ", _ply,
          " | Population: ", _population,
          " | Time-limit: ", _time_limit,
          " | Generation-limit: ", _generation_limit,
          " | Evaluation-limit: ", _evaluation_limit)

    print("\nElapsed generation time: ", time_, " seconds\n")

if __name__ == '__main__':
    Main()
