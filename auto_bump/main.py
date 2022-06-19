"""
Primary module
"""

import os
import sys
from pathlib import Path
from subprocess import run, PIPE, STDOUT


import yaml


def increment_patch(version):
    return [version[0], version[1], version[2] + 1]


def increment_minor(version):
    return [version[0], version[1] + 1, version[2]]


def increment_major(version):
    return [version[0] + 1, version[1], version[2]]


ACTION_PATH = Path(os.environ["GITHUB_ACTION_PATH"])
ENV_PATH = ACTION_PATH / ".black-env"
ENV_BIN = ENV_PATH / ("Scripts" if sys.platform == "win32" else "bin")
CHART = os.environ.get("CHART_NAME")
STRATEGY = os.environ.get("BUMP_STRATEGY", "PATCH")

run([sys.executable, "-m", "venv", str(ENV_PATH)], check=True)
pip_process = run(
    [str(ENV_BIN / "python"), "-m", "pip", "install", "PyYAML"],
    stdout=PIPE,
    stderr=STDOUT,
    encoding="utf-8"
)

if pip_process.returncode:
    print(pip_process.stdout)
    print("::error::Failed to install dependencies", flush=True)
    sys.exit(pip_process.returncode)


long_option = Path(f"./{CHART}/Chart.yaml").resolve()
short_option = Path(f"./{CHART}/Chart.yml").resolve()

file_path = long_option if long_option.is_file() else short_option if short_option.is_file() else False

if file_path:
    print("Found Chart file  at the following path:\n"
          "%s" % file_path)

    with open(file_path) as in_stream:
        f_str = in_stream.read()
        print("Chart Contents:\n"
              "%s" % f_str)
        chart_file = yaml.safe_load(f_str)
        in_stream.close()

    if "version" in chart_file:
        current_version = chart_file["version"]
        os.environ["FIRST_MATE_OLD_VERSION"] = chart_file["version"]
        current_version = [int(v) for v in current_version.split(".")]

        if STRATEGY.upper() == "PATCH":
            new_version = "".join("%s." % str(a) for a in increment_patch(current_version))

        elif STRATEGY.upper() == "MINOR":
            new_version = "".join("%s." % str(a) for a in increment_minor(current_version))

        elif STRATEGY.upper() == "MAJOR":
            new_version = "".join("%s." % str(a) for a in increment_major(current_version))

        else:
            raise ValueError("bump_strategy is not correctly set.")

        print("Version will be bumped to: "
              "%s" % new_version)

        os.environ["FIRST_MATE_NEW_VERSION"] = new_version

        chart_file["version"] = new_version[:-1] if new_version[-1] == "." else new_version

        with open(file_path, "w") as out_stream:
            yaml.dump(chart_file, out_stream, default_flow_style=False, sort_keys=False)
            out_stream.close()

    else:
        raise AttributeError("Helm Chart %s is not properly configured" % CHART)

else:
    raise TypeError("Chart File can not be found in %s chart package." % CHART)
