"""Project 2: diagnose the assignment's Bayesian network by prompting NRP.

Set OPENAI_API_KEY to your NRP key outside this file. No Bayesian inference
library or precomputed answer table is used to produce a diagnosis.
"""

import json
import math
import os

from openai import APIError, OpenAI


NETWORK_PROMPT = """Solve this specific Bayesian-network probability exercise.
Use only the network below, not general medical knowledge.
All eight variables are Boolean. For each table, omitted false probabilities
are 1 minus the stated true probability. Asia and Smoking are independent roots.
The joint probability factorizes as:
P(A,S,T,C,B,E,X,D) = P(A) P(S) P(T|A) P(C|S) P(B|S)
                    P(E|T,C) P(X|E) P(D|E,B).

Definitions and COMPLETE conditional probability tables:
A = visit to Asia: P(A=true)=0.01.
S = smoking: P(S=true)=0.5.
T = TB: P(T=true|A=true)=0.05; P(T=true|A=false)=0.01.
C = Cancer: P(C=true|S=true)=0.1; P(C=true|S=false)=0.01.
B = Bronchitis: P(B=true|S=true)=0.6; P(B=true|S=false)=0.3.
E = TB or Cancer (deterministic OR):
  P(E=true|T=true,C=true)=1; P(E=true|T=true,C=false)=1;
  P(E=true|T=false,C=true)=1; P(E=true|T=false,C=false)=0.
X = abnormal Xray: P(X=true|E=true)=0.99; P(X=true|E=false)=0.05.
D = present Dyspnea:
  P(D=true|E=true,B=true)=0.9; P(D=true|E=true,B=false)=0.7;
  P(D=true|E=false,B=true)=0.8; P(D=true|E=false,B=false)=0.1.

Evidence values: Yes/Abnormal/Present mean true; No/Normal/Absent mean false.
NA means UNKNOWN: sum over both values of that variable; never assume false.
Compute P(T=true|evidence), P(C=true|evidence), P(B=true|evidence).
For each disease H, use P(H=true,evidence)/P(evidence), summing the
factorized joint over every unobserved variable, including other diseases.
Work through the marginalization carefully before answering. Diseases can
coexist, so do NOT normalize these three disease probabilities to sum to 1.
Select the largest posterior, even if it is below 0.5. If tied, prefer TB,
then Cancer, then Bronchitis. Report that posterior, NOT confidence in an answer.
Return ONLY a JSON object with exactly two keys:
{"disease": "TB or Cancer or Bronchitis", "probability": 0.123456}
The disease value must be exactly TB, Cancer, or Bronchitis. Probability must
be a JSON number between 0 and 1, expressed as a decimal, not a percentage.
Use at least six decimal places when needed. No prose or Markdown fences.
"""

_ALLOWED = (
    ("Yes", "No", "NA"),
    ("Yes", "No", "NA"),
    ("Abnormal", "Normal", "NA"),
    ("Present", "Absent", "NA"),
)
_FIELDS = ("visit_to_asia", "smoking", "xray_result", "dyspnea")


def _parse_response(content):
    """Validate the model's answer before handing it to the supplied GUI."""
    if not isinstance(content, str) or not content.strip():
        raise ValueError("The LLM returned no diagnosis text.")
    text = content.strip()
    # Tolerate a single Markdown fence, while still requiring a JSON object.
    lines = text.splitlines()
    if len(lines) >= 3 and lines[0].lower() in ("```", "```json") and lines[-1] == "```":
        text = "\n".join(lines[1:-1])
    try:
        answer = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError("The LLM response was not valid JSON. Try the diagnosis again.") from None
    if not isinstance(answer, dict) or set(answer) != {"disease", "probability"}:
        raise ValueError("Expected only disease and probability in the LLM response.")
    disease, probability = answer["disease"], answer["probability"]
    if disease not in ("TB", "Cancer", "Bronchitis"):
        raise ValueError("The LLM returned an unsupported disease name.")
    if (isinstance(probability, bool) or not isinstance(probability, (int, float))
            or not 0 <= probability <= 1 or not math.isfinite(probability)):
        raise ValueError("The LLM probability must be a finite number between 0 and 1.")
    return [disease, float(probability)]


class Diagnostics:
    """Use an LLM to calculate the assignment network's disease posteriors."""

    def __init__(self):
        # Importing this module and constructing this class make no API calls.
        self.model = os.environ.get("NRP_MODEL", "gpt-oss")
        self.client = None

    def diagnose(self, visit_to_asia, smoking, xray_result, dyspnea):
        values = (visit_to_asia, smoking, xray_result, dyspnea)
        for name, value, allowed in zip(_FIELDS, values, _ALLOWED):
            if value not in allowed:
                raise ValueError(f"{name} must be one of {', '.join(allowed)}.")
        evidence = dict(zip(_FIELDS, values))
        print("Step 1 - Evidence:", json.dumps(evidence), flush=True)

        # The environment stores the NRP-issued credential, never this source file.
        if self.client is None:
            key = os.environ.get("OPENAI_API_KEY", "").strip()
            if not key:
                raise RuntimeError("Set OPENAI_API_KEY to your NRP-issued key, then try again.")
            self.client = OpenAI(
                api_key=key,
                base_url="https://ellm.nrp-nautilus.io/v1",
                timeout=120.0,
                max_retries=0,
            )
        print(f"Step 2 - Requesting {self.model} with the complete network and evidence.", flush=True)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": NETWORK_PROMPT},
                    {"role": "user", "content": "Diagnose this evidence: " + json.dumps(evidence)},
                ],
                temperature=0,
                max_tokens=8192,
            )
        except APIError as error:
            # Avoid printing SDK error bodies, request headers, or credentials.
            raise RuntimeError(
                f"NRP request failed ({type(error).__name__}). Check your NRP key, "
                "network, and model availability. No diagnosis was produced."
            ) from None
        if not response.choices:
            raise ValueError("The LLM returned no choices.")
        choice = response.choices[0]
        if choice.finish_reason != "stop":
            raise ValueError("The LLM response was incomplete or refused. Try again.")
        content = choice.message.content
        print("Step 3 - LLM response:", content, flush=True)
        result = _parse_response(content)
        print(f"Step 4 - Diagnosis: {result[0]} with chance {result[1] * 100:.2f}%", flush=True)
        return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    for name, allowed in zip(_FIELDS, _ALLOWED):
        parser.add_argument(name, nargs="?", default="NA", choices=allowed)
    arguments = parser.parse_args()
    try:
        print("Returned list:", Diagnostics().diagnose(*(getattr(arguments, name) for name in _FIELDS)))
    except (RuntimeError, ValueError) as error:
        parser.exit(1, f"Diagnosis failed: {error}\n")
