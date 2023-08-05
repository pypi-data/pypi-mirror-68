#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import subprocess

from setuptools import setup
from setuptools.command.sdist import sdist as sdist_orig


ROOT = os.path.dirname(__file__)
VERSION = os.path.join(ROOT, "VERSION")


def main():
    return setup(
        # fmt: off
        cmdclass={
            "sdist": sdist,
        },
        version=project_version(),
        # fmt: on
    )


def project_version():
    version = None

    if not version:
        try:
            output = (
                subprocess.check_output(
                    ["git", "describe", "--tags", "--always"],
                    stderr=open(os.devnull, "wb"),
                )
                .strip()
                .decode()
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Can't read the tag. That's probably project at initial stage,
            # or git is not available at all or something else.
            pass
        else:
            try:
                base, distance, commit_hash = output.split("-")
            except ValueError:
                # We're on release tag.
                version = output
            else:
                # Reformat git describe for PEP-440
                version = "{}.{}+{}".format(base, distance, commit_hash)

    if not version and os.path.exists(VERSION):
        with open(VERSION) as verfile:
            version = verfile.read().strip()

    if not version:
        raise RuntimeError("cannot detect project version")

    return version


class sdist(sdist_orig):
    def run(self):
        # In case when user didn't eventually run `make version` ensure that
        # VERSION file will be included in source distribution.
        version = project_version()
        with open(VERSION, "w") as verfile:
            verfile.write(version)
        sdist_orig.run(self)


if __name__ == "__main__":
    main()
