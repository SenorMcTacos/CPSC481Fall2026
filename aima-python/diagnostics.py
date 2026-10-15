import sys

from aima.probability import *
# from probability import *

T, F = True, False


class Diagnostics:
    """Use a Bayesian network to diagnose between three lung diseases"""

    # disease_list = ["TB", "Cancer", "Bronchitis"]

    def __init__(
        self,
    ): ...  # placeholder for the student's code, to be replaced by the student
    def diagnose(self, asia, smoking, xray, dyspnea):
        # Implement
        return ["disease", -1.0]


if __name__ == "__main__":
    pass
