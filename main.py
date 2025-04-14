import os
from multiprocessing import freeze_support
from common.conditions import Conditions
from genetic import Composer
from genetic import FullBoard
import cmd

from genetic.utility import chess_int_to_board


class Main(cmd.Cmd):
    prompt = 'ChessPuzzleGeneration>> '
    intro = 'Welcome to the ChessPuzzleGenerator! Type "help" or "?" to list commands.'

    def __init__(self):
        super().__init__()

    def do_quit(self, args):
        """Quits the program."""
        return True

    def do_run(self, args):
        """Generate a chess puzzle.
        Usage: run <generator-type> <population-size> <time-limit or None> <generation-limit or None> <evaluation-limit or None>
        More info: run help <type>
        """

        args = args.lower().split()
        if len(args) == 0:
            self.do_help("run")
            return

        result = list()

        match args[0]:
            case "help":
                if len(args) > 1:
                    self.__run_help__(args[1])
                    return
            case "composer":
                conditions = self.__format_conditions__(args)
                if conditions is None: return
                result = Composer().run(int(args[1]), conditions)
            case "fullboard":
                conditions = self.__format_conditions__(args)
                if conditions is None: return
                result = FullBoard().run(int(args[1]), conditions)
            case _:
                print("Unknown generator type.")
                return

        if len(args) < 5:
            print("- Insufficient number of arguments.\n"
                  "- Usage: run <generator-type> <population-size> <time-limit or None> <generation-limit or None> <evaluation-limit or None>\n"
                  "- More info: run help <type>")
            return

        for c in result:
            board = chess_int_to_board(c.body)
            print(board.fen())
        return

    def __format_conditions__(self, args: list[str]) -> Conditions | None:
        if len(args) < 5:
            print("- Insufficient number of arguments.\n"
                  "- Usage: run <generator-type> <population-size> <time-limit or None> <generation-limit or None> <evaluation-limit or None>\n"
                  "- Example: run composer 100 None 100 None")
            return None
        aux = []
        for arg in args[2:]:
            if arg == 'none':
                aux.append(None)
            else: aux.append(float(arg))
        return Conditions(aux[0], aux[1], aux[2])

    def __run_help__(self, arg):
        match arg:
            case "generator-type" | "generator":
                print("Available generator types:\n"
                      "==========================\n"
                      "FullBoard | Composer\n"
                      "- FullBoard: Initialises a standard chess board. Randomly moves pieces.\n"
                      "- Composer: Initialises a chess board with each king in some random, valid position. Randomly adds pieces.\n")
            case "population-size" | "population":
                print("Population size: How many boards to initialise.\n"
                      "- A generation will always keep this population size.")
            case "time-limit" | "time":
                print("Time limit: How long the generator will run in seconds.")
            case "generation-limit" | "generation":
                print("Generation limit: How many changes a board will undergo.")
            case "evaluation-limit" | "evaluation":
                print("Evaluation limit: The average score a generation of boards may get.")
            case _:
                print("Unknown argument type. Try 'run help'.")
        return

    def postloop(self):
        print("Have a nice day!")

    def postcmd(self, stop, args):
        print()
        return stop

if __name__ == '__main__':
    freeze_support()
    Main().cmdloop()
