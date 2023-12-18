"""
Module providing utility functions for working with the
Gradescope autograder.

- gen_gradescope_output: Generates a JSON file that can be consumed
    by Gradescope's autograder
"""

import json
from typing import TextIO, Optional


def gen_gradescope_output(
    gradescope_f: TextIO, score: float, output: Optional[bool] = None
) -> None:
    """
    Generates JSON file that can be consumed by Gradescope's autograder.

    Args:
        gradescope_f: Gradescope results file
        score: Score to report
        output: Optional output to be shown by the autograder

    Returns: None

    """
    gradescope_json: dict[str, str | float] = {}
    gradescope_json["score"] = score
    if output is not None:
        gradescope_json["output"] = output
    gradescope_json["visibility"] = "visible"
    gradescope_json["stdout_visibility"] = "visible"
    json.dump(gradescope_json, gradescope_f, indent=2)
