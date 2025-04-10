class Conditions:
    def __init__(self, time_limit=float("inf"), generation_limit=float("inf"), evaluation_limit=float("inf")):
        self.time_limit = time_limit if time_limit is not None else float("inf")
        self.generation_limit = generation_limit if generation_limit is not None else float("inf")
        self.evaluation_limit = evaluation_limit if evaluation_limit is not None else float("inf")