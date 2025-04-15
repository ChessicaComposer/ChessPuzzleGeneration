from collections import defaultdict
import cli_ui
from common.conditions import Conditions
from genetic import FullBoard, Composer
from genetic.utility import chess_int_to_board

def is_nonzero_int(arg: str | None) -> bool:
    if arg is None or not arg.isdigit() or int(arg) < 1:
        return False
    return True

def print_args(generator, ply, population, limits) -> None:
      print("Generator: ", generator,
          " | Ply: ", ply,
          " | Population: ", population,
          " | Time-limit: ", limits["time"],
          " | Generation-limit: ", limits["generation"],
          " | Evaluation-limit: ", limits["evaluation"])

def welcome() -> None:
    cli_ui.info_section("\nChessPuzzleGeneration :: Using Genetic Algorithms")
    cli_ui.info("Configure the generator by answering the following.\n")

def get_ply(generator):
    if generator != "FullBoard":
        return int(cli_ui.ask_string("Choose ply"))
    else:
        cli_ui.info_2("FullBoard has a default ply of 5.")
        return 5

@cli_ui.Timer("FullBoard")
def run_fullboard(population, conditions) -> list:
    return FullBoard().run(int(population), conditions)

@cli_ui.Timer("Composer")
def run_composer(ply, population, conditions) -> list:
    return Composer(ply).run(int(population), conditions)


def main():
    cli_ui.setup(color="always")
    welcome()

    cli_ui.info_count(0, 3, "Required questions")
    generators = ["FullBoard", "Composer"]
    chosen_generator = cli_ui.ask_choice("Choose a generator", choices=generators, sort=False)
    print()

    cli_ui.info_count(1, 3, "Required questions")
    ply = get_ply(chosen_generator)
    print()

    cli_ui.info_count(2, 3, "Required questions")
    chosen_population = cli_ui.ask_string("Choose population size")
    if not is_nonzero_int(chosen_population):
        cli_ui.info("Please enter a non-zero integer.")
        exit(1)
    print()

    cli_ui.info_2("The following questions are optional")
    limits: defaultdict[str, float | None] = defaultdict()
    limits["time"] = cli_ui.ask_string("Choose time-limit in seconds")
    print()

    limits["generation"] = cli_ui.ask_string("Choose generation-limit")
    print()

    limits["evaluation"] = cli_ui.ask_string("Choose evaluation limit")

    for limit in limits:
        if not is_nonzero_int(limits[limit]):
            limits[limit] = None
        else:
            limits[limit] = float(limits[limit])

    conditions = Conditions(limits["time"], limits["generation"], limits["evaluation"])

    result = []

    cli_ui.info(cli_ui.blue, "------------------------")

    match chosen_generator:
        case "FullBoard":
            result = run_fullboard(chosen_population, conditions)
        case "Composer":
            result = run_composer(ply, chosen_population, conditions)
        case _:
            raise ValueError
    cli_ui.info(cli_ui.blue, "------------------------")

    for res in result:
        board = chess_int_to_board(res.body)
        print(board.fen())

    cli_ui.info(cli_ui.blue, "------------------------")
    print_args(chosen_generator, ply, chosen_population, limits)


if __name__ == '__main__':
    main()
