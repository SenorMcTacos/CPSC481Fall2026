import sys

from aima.probability import *
# from probability import *

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://ellm.nrp-nautilus.io/v1",
)

completion = client.chat.completions.create(
    model="gpt-oss",
    messages=[
        {"role": "system", "content": "Talk like a pirate."},
        {
            "role": "user",
            "content": "How do I check if a Python object is an instance of a class?",
        },
    ],
)

print(completion.choices[0].message.content)

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
