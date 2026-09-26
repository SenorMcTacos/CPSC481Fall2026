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
        # bayes_net = BayesNet("Asia")
        # bayes_net.add("")
        # bayes_net.add("Asia")
        # bayes_net.add("Smoking")
        # bayes_net.add("Xray")
        # bayes_net.add("Dyspnea")

    def diagnose(self, asia, smoking, xray, dyspnea):
        # To be implemented by the student

        # Create Bayes Network
        cancer_bayes = BayesNet(
            [
                ("Asia", "", 0.01),
                ("Smoking", "", 0.5),
                ("TB", "Asia", {T: 0.05, F: 0.1}),
                ("LungCancer", "Smoking", {T: 0.1, F: 0.01}),
                ("Bronchitis", "Smoking", {T: 0.6, F: 0.3}),
                (
                    "TBorCancer",
                    "TB LungCancer",
                    {(T, T): 1.0, (T, F): 1.0, (F, T): 1.0, (F, F): 0},
                ),
                ("Xray", "TBorCancer", {T: 0.99, F: 0.05}),
                (
                    "Dyspnea",
                    "TBorCancer Bronchitis",
                    {(T, T): 0.9, (T, F): 0.7, (F, T): 0.8, (F, F): 0.1},
                ),
            ]
        )

        # Convert function variables to booleans
        asia_c = convert_to_bool(asia)
        smoking_c = convert_to_bool(smoking)
        xray_c = convert_to_bool(xray)
        dyspnea_c = convert_to_bool(dyspnea)
        # print(asia_c, smoking_c, xray_c, dyspnea_c)

        # Calculate disease with highest chance
        tb_chance = diagnose_enumerate_ask(
            "TB", asia_c, smoking_c, xray_c, dyspnea_c, cancer_bayes
        )
        lc_chance = diagnose_enumerate_ask(
            "LungCancer", asia_c, smoking_c, xray_c, dyspnea_c, cancer_bayes
        )
        br_chance = diagnose_enumerate_ask(
            "Bronchitis", asia_c, smoking_c, xray_c, dyspnea_c, cancer_bayes
        )

        if tb_chance > lc_chance and tb_chance > br_chance:
            return ["TB", tb_chance]
        elif lc_chance > tb_chance and lc_chance > br_chance:
            return ["Lung Cancer", tb_chance]
        elif br_chance > lc_chance and br_chance > tb_chance:
            return ["Bronchitis", tb_chance]
        else:
            return ["Error", 0]


def convert_to_bool(input):
    if input == "Yes" or input == "Present" or input == "Abnormal":
        return T
    else:
        return F


def diagnose_enumerate_ask(disease_to_find, asia, smoking, xray, dyspnea, bn):
    calc = enumeration_ask(
        disease_to_find,
        dict(Asia=asia, Smoking=smoking, Dyspnea=dyspnea, Xray=xray),
        bn,
    )[T]

    return calc


if __name__ == "__main__":
    test = BayesNet(
        [
            ("Test", "", 0.1),
            ("Balls", "", 0.1),
            ("TB", "Test", {T: 0.05, F: 0.1}),
            ("TBA", "Balls", {T: 0.05, F: 0.1}),
        ]
    )
    cancer_bayes_2 = BayesNet(
        [
            ("Asia", "", 0.01),
            ("Smoking", "", 0.5),
            ("TB", "Asia", {T: 0.05, F: 0.1}),
            ("LungCancer", "Smoking", {T: 0.1, F: 0.01}),
            ("Bronchitis", "Smoking", {T: 0.6, F: 0.3}),
            (
                "TBorCancer",
                "TB LungCancer",
                {(T, T): 1.0, (T, F): 1.0, (F, T): 1.0, (F, F): 0},
            ),
            ("Xray", "TBorCancer", {T: 0.99, F: 0.05}),
            (
                "Dyspnea",
                "TBorCancer Bronchitis",
                {(T, T): 0.9, (T, F): 0.7, (F, T): 0.8, (F, F): 0.1},
            ),
        ]
    )
    cloudy_bn = BayesNet(
        [
            ("Cloudy", "", 0.75),
            ("Freezing", "", 0.333),
            (
                "Accident",
                "Cloudy Freezing",
                {(T, T): 0.8, (T, F): 0.5, (F, T): 0.6, (F, F): 0.1},
            ),
        ]
    )
    # print(enumeration_ask("Asia", dict(Smoking=T), cancer_bayes_2))
    # print(enumeration_ask("Test", dict(), test).show_approx())
    # print(enumeration_ask("Accident", dict(Cloudy=T, Freezing=T), cloudy_bn)[T])
    # print(elimination_ask("Accident", dict(Cloudy=T, Freezing=T), cloudy_bn)[T])
    print(
        enumeration_ask(
            "TB", dict(Asia=T, Smoking=T, Xray=T, Dyspnea=T), cancer_bayes_2
        )[T]
    )

    balls = Diagnostics()
    print(balls.diagnose("Yes", "Yes", "Abnormal", "Present"))
    # print(enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary))
    # print(enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary)[T])
    # print(burglary.variable_node('Burglary').p(T, {}))
    # print(burglary.vari
