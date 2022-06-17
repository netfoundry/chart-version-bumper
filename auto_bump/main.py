"""
Primary module
"""

from pathlib import Path
import os

import yaml

from .utils import increment_patch, increment_major, increment_minor

chart = os.environ.get("CHART_NAME")
strategy = os.environ.get("BUMP_STRATEGY", "PATCH")


def main(chart_name=chart, bump_strategy=strategy):

    long_option = Path(f"./{chart_name}/Chart.yaml").resolve()
    short_option = Path(f"./{chart_name}/Chart.yml").resolve()

    file_path = long_option if long_option.is_file() else short_option if short_option.is_file() else False

    if file_path:

        file = open(file_path, "w+")
        chart_file = yaml.safe_load(file)

        if "version" in chart_file:
            current_version = chart_file["version"]
            current_version = [int(v) for v in current_version.split(".")]

            if bump_strategy.upper() == "PATCH":
                new_version = "".join("%s." % str(a) for a in increment_patch(current_version))

            elif bump_strategy.upper() == "MINOR":
                new_version = "".join("%s." % str(a) for a in increment_minor(current_version))

            elif bump_strategy.upper() == "MAJOR":
                new_version = "".join("%s." % str(a) for a in increment_major(current_version))

            else:
                raise ValueError("bump_strategy is not correctly set.")

            chart_file["version"] = new_version

            with open("modified.yml", "w") as out_stream:
                yaml.dump(chart_file, out_stream, default_flow_style=False, sort_keys=False)

        else:
            raise AttributeError("Helm Chart %s is not properly configured" % chart_name)

    else:
        raise TypeError("Chart File can not be found in %s chart package." % chart_name)
