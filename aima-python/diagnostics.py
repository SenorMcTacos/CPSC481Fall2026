import sys

from aima.probability import *
# from probability import *

T, F = True, False


class Diagnostics:
    """Use a Bayesian network to diagnose between three lung diseases"""

    disease_list = ["TB", "Cancer", "Bronchitis"]

    def __init__(
        self,
    ):
        ...  # placeholder for the student's code, to be replaced by the student
        bayes_net = BayesNet("Asia")
        # bayes_net.add("")
        bayes_net.add("Asia")
        bayes_net.add("Smoking")
        bayes_net.add("Xray")
        bayes_net.add("Dyspnea")

    def diagnose(self, asia, smoking, xray, dyspnea):
        # To be implemented by the student
        # example
        # burglary = BayesNet([
        # ('Burglary', '', 0.001),
        # ('Earthquake', '', 0.002),
        # ('Alarm', 'Burglary Earthquake',
        # {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
        # ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
        # ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})
        # ]

        cancer_bayes = BayesNet(
            [
                ("Asia", "", 0.01),
                ("Smoking", "", 0.5),
                ("TB", "Asia", {T: 0.05, F: 0.1}),
                ("Lung Cancer", "Smoking", {T: 0.1, F: 0.01}),
                ("Bronchitis", "Smoking", {T: 0.6, F: 0.3}),
                (
                    "TB or Cancer",
                    "Tuberculosis Lung Cancer",
                    {(T, T): 1.0, (T, F): 1.0, (F, T): 1.0, (F, F): 0},
                ),
                ("X-ray", "TB or Cancer", {T: 0.99, F: 0.05}),
                (
                    "Dyspnea",
                    "TB or Cancer Bronchitis",
                    {(T, T): 0.9, (T, F): 0.7, (F, T): 0.8, (F, F): 0.1},
                ),
            ]
        )
        return [
            "the disease",
            1.0,
        ]  # placeholder return value, to be replaced by the student
