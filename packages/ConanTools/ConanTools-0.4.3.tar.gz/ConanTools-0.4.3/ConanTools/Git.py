"""Support module for querying git.

This module provides a few simple methods to deduce information like the current revision, the name
of the current tag, or potential branch names from a git repository. We call git using a subprocess
to the deduce the needed information which means that a shell installation of git is required to
use this module.
"""
from collections import OrderedDict
import os
from pathlib import Path
from subprocess import run, PIPE, DEVNULL
from typing import List, Optional


def revision(cwd: Optional[str] = None) -> Optional[str]:
    res = run(["git", "rev-parse", "HEAD"],
              stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, universal_newlines=True, cwd=cwd)
    if res.returncode == 0:
        return res.stdout.strip()
    return None


def branches(rev: Optional[str] = None, cwd: Optional[str] = None) -> List[str]:
    result = []
    current_sha = rev or revision(cwd=cwd)
    # Get a list of all heads and their SHAs.
    refs = run(["git", "for-each-ref", "--format=%(objectname) %(refname:short)", "refs/heads"],
               stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, universal_newlines=True, cwd=cwd,
               check=True).stdout.strip()
    if refs != "":
        refs = [line.split(' ', 1) for line in refs.replace('\r', '').split('\n')]
        result.extend([name for sha, name in refs if sha == current_sha])
    # Also inspect remote refs for matching names.
    refs = run(["git", "for-each-ref", "--format=%(objectname) %(refname)", "refs/remotes"],
               stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, universal_newlines=True, cwd=cwd,
               check=True).stdout.strip()
    if refs != "":
        refs = [line.split(' ', 1) for line in refs.replace('\r', '').split('\n')]
        # Strip the first 3 components from the ref to get the branch name
        # (newer git versions have "--format=%(objectname) %(refname:lstrip=3)")
        result.extend([os.path.join(*Path(name).parts[3:])
                       for sha, name in refs if sha == current_sha])
    # Return the list of found names without duplicates.
    return list(OrderedDict.fromkeys(result))


def branch(cwd: Optional[str] = None) -> Optional[str]:
    res = branches(cwd=cwd)
    # Skip variants of "head" when we have more options because it is ususally not a useful name.
    while len(res) > 1 and res[0].lower() == "head":
        res.pop(0)
    if len(res) > 0:
        return res[0]
    return None


def describe(cwd: Optional[str] = None) -> Optional[str]:
    res = run(["git", "describe", "--tags", "--abbrev=40", "--always"],
              stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, universal_newlines=True, cwd=cwd)
    if res.returncode == 0:
        return res.stdout.strip()
    return None


def is_repository(cwd: Optional[str] = None) -> bool:
    return run(["git", "status"],
               stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, cwd=cwd).returncode == 0


def tag(cwd: Optional[str] = None) -> Optional[str]:
    res = run(["git", "describe", "--exact-match", "--tags"],
              stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, universal_newlines=True, cwd=cwd)
    if res.returncode == 0:
        return res.stdout.strip()
    return None
