"""
Command for validating a CS 142 repository.

Will perform the following checks:

- The repository contains the following files:
  - README.md
  - hw0/README.md
  - hw0/README-TOO.md
- The README.md file has been edited as specified
  in Homework #0
- The README-TOO.md contains the text specified
  in Homework #0

When run locally (not on Gradescope), it will
also check that the directory that the program
is contained inside a Git repository, and that
it has the correct remotes set up.

"""
import os
from pathlib import Path


import click

from validators import (
    FileExistsValidator,
    FileContainsValidator,
    FileDoesntContainValidator,
    GitRepoValidator,
    GitRepoFileValidator,
    GitRepoRemoteValidator,
)

from common import gen_gradescope_output


@click.command(name="validate-repo")
@click.option("--gradescope", type=click.File("w"))
@click.option("--base-dir", type=click.Path(exists=True, file_okay=False))
def cmd(gradescope, base_dir):
    if base_dir is not None:
        repo_dir = Path(base_dir)
    else:
        repo_dir = Path(os.path.abspath(__file__)).parent.parent

    readme_exists = FileExistsValidator(repo_dir, "README.md")
    readme_edited1 = FileDoesntContainValidator(
        repo_dir,
        "README.md",
        "This is the upstream repository for CMSC 14200.",
        hint="Remember you need to edit this file.",
        depends=[readme_exists],
    )
    readme_edited2 = FileDoesntContainValidator(
        repo_dir,
        "README.md",
        "This is the repository for FULL_NAME (CNETID)",
        hint="Remember to replace FULL_NAME and CNETID with your full name and CNetID",
        depends=[readme_edited1],
    )
    readme_edited3 = FileContainsValidator(
        repo_dir,
        "README.md",
        r"This is the repository for [^\(\)]+ \(.*\)",
        regex=True,
        hint="You must edit this file so the line starting with 'This is the repository' "
        "contains the text 'This is the repository for FULL_NAME (CNETID)'",
        depends=[readme_edited2],
    )

    validators = [readme_exists, readme_edited1, readme_edited2, readme_edited3]

    hw0readme_exists = FileExistsValidator(repo_dir, "hw0/README.md")
    hw0readme_contents = FileContainsValidator(
        repo_dir,
        "hw0/README.md",
        "# Homework #0",
        hint="You should not edit this file.",
        depends=[hw0readme_exists],
    )

    hw0readmetoo_exists = FileExistsValidator(
        repo_dir,
        "hw0/README-TOO.md",
        hint="Did you forget to create it, or add it to your repository?",
    )
    hw0readmetoo_contents = FileContainsValidator(
        repo_dir,
        "hw0/README-TOO.md",
        "Please read me too!",
        exact=True,
        depends=[hw0readmetoo_exists],
    )

    validators += [
        hw0readme_exists,
        hw0readme_contents,
        hw0readmetoo_exists,
        hw0readmetoo_contents,
    ]

    if gradescope is None:
        # We only do these checks if we're not running inside Gradescope
        is_repo = GitRepoValidator(repo_dir)

        readme_added = GitRepoFileValidator(
            repo_dir,
            "README.md",
            hint="Remember to 'git add' and 'git commit' it",
            depends=[is_repo, readme_exists],
        )
        readme2_added = GitRepoFileValidator(
            repo_dir,
            "hw0/README-TOO.md",
            hint="Remember to 'git add' and 'git commit' it",
            depends=[is_repo, hw0readmetoo_exists],
        )
        origin_remote = GitRepoRemoteValidator(
            repo_dir, "origin", "REPO_URL", check_url_equality=False, depends=[is_repo]
        )
        origin_upstream = GitRepoRemoteValidator(
            repo_dir,
            "upstream",
            "git@github.com:uchicago-cmsc14200-win-2024/coursework-upstream.git",
            depends=[is_repo],
        )

        validators += [is_repo, readme_added, readme2_added, origin_remote, origin_upstream]

    if all(v.valid for v in validators):
        if gradescope is None:
            print("Your repository appears to be correctly set up.")
            print("Don't forget to submit it on Gradescope!")
        else:
            print("The files you have submitted appear to be correct.")
            print()
            print("Don't forget to click on the 'Code' tab to double-check")
            print("that all your files are there. You should do this in all")
            print("your homework submissions!")
            gen_gradescope_output(gradescope, 1.0)
    else:
        if gradescope is None:
            print("There are a few issues with your repository:\n")
        else:
            print("There are a few issues with your submitted files:\n")

        for v in validators:
            if v.valid is not None and not v.valid:
                print("-", v.error_msg, "\n")

        if gradescope is not None:
            gen_gradescope_output(
                gradescope,
                0.0,
                output="Make sure to address the above issues, and to resubmit your repository",
            )


if __name__ == "__main__":
    cmd()
