#!/usr/bin/env python3

from pathlib import Path
import papermill
import click
import sys


@click.command()
@click.option("--dir", default=".", help="Dir to run in. Defaults to: .")
@click.option(
    "--out", default="ci_out/", help="Where to store output? Defaults to: ./out/"
)
def run_notebooks(dir, out):
    """Run all notebooks in dir and stores them in out."""
    # make dirs paths
    dir = Path(dir)
    out = Path(out)

    # find all notebooks in dir
    # except for those already in out, checkpoints, and those marked as NOCIRUN
    notebooks = dir.glob("**/*.ipynb")
    notebooks = filter(lambda f: out.resolve() not in f.resolve().parents, notebooks)
    notebooks = filter(lambda f: ".ipynb_checkpoint" not in str(f), notebooks)
    notebooks = filter(lambda f: "NOCIRUN" not in f.name, notebooks)
    notebooks = sorted(notebooks)

    # run all notebooks, keeping track of success
    something_failed = False
    for nb in notebooks:
        output_nb = out / nb
        output_nb.parent.mkdir(parents=True, exist_ok=True)
        try:
            print(f"will run {str(nb)}", flush=True)
            papermill.execute_notebook(str(nb), str(output_nb), cwd=str(nb.parent))
        except Exception as e:
            print(f"\n{nb} failed", flush=True)
            something_failed = True

    sys.exit(something_failed)  # returns 0 if everything worked


if __name__ == "__main__":
    run_notebooks()
