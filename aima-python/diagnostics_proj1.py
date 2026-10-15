import sys

from aima.probability import *
# from probability import *

T, F = True, False


class Diagnostics:
    """Use a Bayesian network to diagnose between three lung diseases"""

    disease_list = ["TB", "Cancer", "Bronchitis"]

    def __init__(
        self,
    ): ...  # placeholder for the student's code, to be replaced by the student
    def diagnose(self, asia, smoking, xray, dyspnea):
        # To be implemented by the student

        # Create Bayes Network
        cancer_bayes = BayesNet(
            [
                ("Asia", "", 0.01),
                ("Smoking", "", 0.5),
                ("TB", "Asia", {T: 0.05, F: 0.01}),
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
        tborc_chance = diagnose_enumerate_ask(
            "TBorCancer", asia_c, smoking_c, xray_c, dyspnea_c, cancer_bayes
        )
        # print(f"Tborc: {tborc_chance}")
        # tb_chance += tborc_chance
        # lc_chance += tborc_chance

        # Evaluate disease for largest chances
        if tb_chance > lc_chance and tb_chance > br_chance:
            return ["TB", tb_chance]
        elif lc_chance > tb_chance and lc_chance > br_chance:
            return [
                "Cancer",
                lc_chance,
            ]  # Apparently it wants the word cancer back instead of Lung Cancer
        elif br_chance > lc_chance and br_chance > tb_chance:
            return ["Bronchitis", br_chance]
        else:
            return ["Error", 0]


def convert_to_bool(input):
    if input == "Yes" or input == "Present" or input == "Abnormal":
        return T
    elif input == "No" or input == "Normal" or input == "Absent":
        return F
    else:
        return "NA"


def diagnose_enumerate_ask(disease_to_find, asia, smoking, xray, dyspnea, bn):
    table_dict: dict = {}
    if asia != "NA":
        table_dict["Asia"] = asia
    if smoking != "NA":
        table_dict["Smoking"] = smoking
    if xray != "NA":
        table_dict["Xray"] = xray
    if dyspnea != "NA":
        table_dict["Dyspnea"] = dyspnea
    calc = enumeration_ask(
        disease_to_find,
        table_dict,
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
    test_cancer_bayes = BayesNet(
        [
            ("Asia", "", 0.01),
            ("Smoking", "", 0.5),
            ("TB", "Asia", {T: 0.05, F: 0.01}),
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

    # print(enumeration_ask("Asia", dict(Smoking=T), cancer_bayes_2))
    # print(enumeration_ask("Test", dict(), test).show_approx())
    # print(enumeration_ask("Accident", dict(Cloudy=T, Freezing=T), cloudy_bn)[T])
    # print(elimination_ask("Accident", dict(Cloudy=T, Freezing=T), cloudy_bn)[T])
    # print(enumeration_ask("TB", dict(), test_cancer_bayes)[T])
    # print(enumeration_ask("LungCancer", dict(), test_cancer_bayes)[T])
    # print(enumeration_ask("Bronchitis", dict(), test_cancer_bayes)[T])

    # balls = Diagnostics()
    # print(balls.diagnose("No", "Yes", "Abnormal", "Present"))
    # print(balls.diagnose("NA", "NA", "NA", "NA"))
    # print(enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary))
    # print(enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary)[T])
    # print(burglary.variable_node('Burglary').p(T, {}))
    # print(burglary.vari
