#!/usr/bin/python3

import click
import configparser
import json
import sys
import os.path
from pathlib import Path

from typing import Dict, Union, List, Tuple

def print_empty_gradescope() -> None:
    gradescope_json: Dict[str, Union[float,str]] = {}
    gradescope_json["score"] = 0.0
    gradescope_json["output"] = "We were unable to run the tests due to an error in your code."
    gradescope_json["visibility"] = "visible"
    gradescope_json["stdout_visibility"] = "visible"
    print(json.dumps(gradescope_json, indent=2))


@click.command(name="grader")
@click.option("--json-file", type=click.STRING, default="tests.json")
@click.option("--rubric-file", type=click.Path(exists=True), default="pytest.ini")
@click.option("--csv", is_flag=True)
@click.option("--gradescope", is_flag=True)
@click.option("--gradescope-visibility", type=click.Choice(["hidden", "after_due_date", "after_published", "visible"]),
                                         default="after_published")
def cmd(json_file: str, rubric_file: Path, csv: bool, gradescope: bool, gradescope_visibility: str) -> None:
    if not os.path.exists(json_file):
        print("No such file: {}".format(json_file), file=sys.stderr)
        print("Make sure you run py.test before running the grader!", file=sys.stderr)

        if gradescope:
            print_empty_gradescope()
        else:
            sys.exit(1)

    with open(json_file) as f:
        results = json.load(f)

    config = configparser.ConfigParser(delimiters=('='))
    config.optionxform = lambda option: option # type: ignore[assignment]
    config.read(rubric_file)

    if "test-points" not in config:
        print("Error: {} does not have a [test-points] section.".format(rubric_file), file=sys.stderr)
        sys.exit(1)

    categories = [[name] + value.split(",") for name, value in config["test-points"].items()]
    category_names = [name for name, _, _ in categories]
    cid2name = {cid: name for name, cid, _ in categories}
    total_points = {name: float(points) for name, _, points in categories}

    thresholds = [[name] + value.split(",") for name, value in config["thresholds"].items()]

    tests: Dict[str, Dict[str, int]] = {cname: {} for cname in category_names}

    for test in results["tests"]:
        test_id = test["nodeid"]
        outcome = test["outcome"]

        # Check that the test only matches a single category
        cid_matches = [cid for cid in cid2name if cid in test_id]
        if len(cid_matches) == 0:
            print("Error: Test {} does not match any category in the rubric.".format(test_id))
            sys.exit(1)
        elif len(cid_matches) > 1:
            print("Error: Test {} matches more than one category in the rubric: {}".format(test_id, ", ".join(cid_matches)))
            sys.exit(1)

        cid = cid_matches[0]
        cname = cid2name[cid]

        if outcome == "passed":
            tests[cname][test_id] = 1
        else:
            tests[cname][test_id] = 0

    empty_categories = [cname for cname in category_names if len(tests[cname]) == 0]

    if gradescope:
        gradescope_json: Dict[str, Union[float,str,List[Dict[str,Union[str,float]]]]] = {}
        gradescope_json["tests"] = []

    if len(empty_categories) > 0:
        print("WARNING: The following categories had no test results:", ", ".join(empty_categories), file=sys.stderr)
        print("         Make sure you run py.test without '-k' before you run the grader\n", file=sys.stderr)

        if gradescope:
            gradescope_json["output"] = "We were unable to run some or all of the tests due to an error in your code."

    scores: Dict[str, Tuple[int, int, int]] = {}
    for cname in category_names:
        num_total = len(tests[cname])
        num_success = sum(tests[cname].values())
        num_failed = num_total - num_success
        scores[cname] = (num_success, num_failed, num_total)

    pscores = []
    pscore = 0.0

    if not csv and not gradescope:
        print("%-62s %-6s / %-10s  %-6s / %-10s" % ("Category", "Passed", "Total", "Score", "Possible"))
        print("-" * 100)

    for cname in category_names:
        (num_success, num_failed, num_total) = scores[cname]

        cpoints = total_points[cname]

        if num_total == 0:
            cscore = 0.0
        else:
            cscore = (float(num_success) / num_total) * cpoints

        pscore += cscore

        if not csv and not gradescope:
            print("%-62s %-6i / %-10i  %-6.2f / %-10.2f" % (cname, num_success, num_total, cscore, cpoints))
        elif gradescope:
            gs_test: Dict[str, Union[str, float]] = {}
            gs_test["score"] = cscore
            gs_test["max_score"] = cpoints
            gs_test["name"] = cname
            assert isinstance(gradescope_json["tests"], list)
            gradescope_json["tests"].append(gs_test)

    if not csv and not gradescope:
        print("-" * 100)
        print("%81s = %-6.2f / %-10i" % ("TOTAL", pscore, sum(total_points.values())))
        overall = pscore/sum(total_points.values()) * 100.0
        snu = "Unsatisfactory"
        for _, name, value in thresholds:
            if overall >= float(value):
                snu = name[1:-1]
        print("%81s = %s" % ("SNU Score", snu))
        print("=" * 100)
        print()

    pscores.append(pscore)

    if csv:
        print(",".join([str(s) for s in pscores]))
    elif gradescope:
        gradescope_json["score"] = pscore
        gradescope_json["visibility"] = gradescope_visibility
        gradescope_json["stdout_visibility"] = gradescope_visibility

        print(json.dumps(gradescope_json, indent=2))

if __name__ == "__main__":
    cmd()