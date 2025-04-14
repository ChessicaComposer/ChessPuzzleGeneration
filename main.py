import time
from multiprocessing import freeze_support
from common.conditions import Conditions
from genetic import Composer
from genetic import FullBoard
import cmd
from genetic.utility import chess_int_to_board


class Main(cmd.Cmd):
    prompt = 'ChessPuzzleGenerator>> '
    intro = ('Welcome to the ChessPuzzleGenerator! Type "help" or "?" to list commands\n'
             '- Usage: run <Composer | FullBoard> <Ply: int> <Population: int> <Time-limit: int | None> <Generation-limit: int | None> <Evaluation-limit: int | None>\n'
             '- Example: run composer 5 100 14400 none none')

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
        time_ = 0.0

        match args[0]:
            case "help":
                if len(args) > 1:
                    self._run_help(args[1])
                    return
            case "composer":
                conditions = self._format_conditions(args)
                if conditions is None: return
                start_time = time.time()
                result = Composer(int(args[1])).run(int(args[2]), conditions)
                time_ = time.time() - start_time
            case "fullboard":
                conditions = self._format_conditions(args)
                if conditions is None: return
                start_time = time.time()
                result = FullBoard(int(args[1])).run(int(args[2]), conditions)
                time_ = time.time() - start_time
            case _:
                print("Unknown generator type.")
                return

        if len(args) < 6:
            self._print_insufficient_args()
            return

        for c in result:
            board = chess_int_to_board(c.body)
            print(board.fen())

        
        self._print_args(args)
        print("Elapsed generation time: ", time_, " seconds")

        return

    def _format_conditions(self, args: list[str]) -> Conditions | None:
        if len(args) < 5:
            self._print_insufficient_args()
            print("- Example: run composer 100 None 100 None")
            return None
        aux = []
        for arg in args[3:]:
            if arg == 'none':
                aux.append(None)
            else: aux.append(float(arg))
        return Conditions(aux[0], aux[1], aux[2])

    def _run_help(self, arg):
        match arg:
            case "generator-type" | "generator" | "composer" | "fullboard":
                print("Available generator types:\n"
                      "==========================\n"
                      "FullBoard | Composer\n"
                      "- FullBoard: Initialises a standard chess board. Randomly moves pieces.\n"
                      "- Composer: Initialises a chess board with each king in some random, valid position. Randomly adds pieces.\n")
            case "ply-size" | "ply":
                print("Ply size: How many moves ahead the generator will evaluate the board's state.")
            case "population-size" | "population":
                print("Population size: How many boards to initialise.\n"
                      "- A generation will always keep this population size.")
            case "time-limit" | "time":
                print("Time limit: How long the generator will run in seconds.\n"
                      "- If time's exceeded, it will finish its current generation before exiting.")
            case "generation-limit" | "generation":
                print("Generation limit: How many changes a board will undergo.")
            case "evaluation-limit" | "evaluation":
                print("Evaluation limit: The average score a generation of boards may get.")
            case _:
                print("Unknown argument type. Try 'run help', ex: 'run help generator'.")
        return

    def _print_insufficient_args(self):
        print("Insufficient number of arguments.\n"
              "===================================\n"
              "- Usage: run <generator-type> <ply-size> <population-size> <time-limit or None> <generation-limit or None> <evaluation-limit or None>\n"
              "- More info: run help <type>")

    def _print_args(self, args):
        generator = args[0]
        ply = args[1]
        population = args[2]
        time_limit = args[3]
        generation_limit = args[4]
        evaluation_limit = args[5]
        print("\n==========================\n",
              "Generator: ", generator,
              " | Ply: ", ply,
              " | Population: ", population,
              " | Time-limit: ", time_limit,
              " | Generation-limit: ", generation_limit,
              " | Evaluation-limit: ", evaluation_limit)


    def postloop(self):
        print("Have a nice day!")

    def postcmd(self, stop, args):
        print()
        return stop

if __name__ == '__main__':
    freeze_support()
    Main().cmdloop()
