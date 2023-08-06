"""
Support code for Tyrannosaurus.
"""

from __future__ import annotations

import enum
import logging
import os
import re
from pathlib import Path
import subprocess
from subprocess import check_output, SubprocessError
from typing import Optional, Union, Sequence, Mapping, Tuple as Tup

import requests
import typer

logger = logging.getLogger(__package__)


class _TrashList:
    def __init__(self, dists: bool, aggressive: bool):
        self.trash_patterns = {
            ".pytest_cache",
            "__pycache__",
            "cython_debug",
            "eggs",
            "__pypackages__",
            "docs/_html",
            "docs/_build",
            re.compile(r".*\.egg-info"),
            re.compile(r".*\.py[cod]"),
            re.compile(r".*\$py\.class"),
            re.compile(r".*\.egg-info"),
        }
        if dists:
            self.trash_patterns.add("dists")
        if aggressive:
            self.trash_patterns.update(
                {
                    ".tox",
                    "poetry.lock" "docs/html",
                    "Thumbs.db",
                    "dist",
                    "sdist",
                    ".ipynb_checkpoints",
                    ".cache",
                    re.compile(r"\*\.swp"),
                    re.compile(r".*[~.]temp"),
                    re.compile(r".*[~.]tmp"),
                }
            )

    def get_list(self) -> Sequence[Path]:
        return [Path(s) for s in self.trash_patterns if isinstance(s, str)]

    def get_patterns(self) -> Sequence[re.Pattern]:
        return [s for s in self.trash_patterns if isinstance(s, re.Pattern)]

    def should_delete(self, p: Path) -> bool:
        return any(
            (
                (
                    isinstance(pattern, str)
                    and str(p).replace("\\", "/").endswith(pattern)
                    or isinstance(pattern, re.Pattern)
                    and pattern.fullmatch(p.name)
                )
                for pattern in self.trash_patterns
            )
        )


class _License(enum.Enum):
    apache2 = "apache2"
    cc0 = "cc0"
    ccby = "cc-by"
    ccbync = "cc-by-nc"
    gpl3 = "gpl3"
    lgpl3 = "lgpl3"
    mit = "mit"

    def full_name(self) -> str:
        return dict(apache2="Apache-2.0", mit="MIT",).get(self.name, "")


class _Env:
    def __init__(self, authors: Optional[Sequence[str]], user: Optional[str]):
        if authors is None:
            self.authors = self._git("user.name").split(",")
        else:
            self.authors = authors
        if user is None:
            self.user = self._git("user.email")
        else:
            self.user = user
        if "@" in self.user:
            self.user = self.user.split("@")[0]

    def _git(self, key: str) -> str:
        try:
            result = check_output(["git", "config", key], encoding="utf8")
        except SubprocessError:
            logger.error("Failed calling git")
            return "<<{}>>".format(key)
        if result is None:
            logger.error("Could not get git config item {}".format(key))
        return "<<{}>>".format(key)


class _InitTomlHelper:
    def __init__(self, name: str, authors: Sequence[str], license_name, username: str):
        self.name = name
        self.authors = authors
        self.license_name = license_name
        self.username = username

    def fix(self, lines: Sequence[str]):
        author_line = "Douglas Myers-Turnbull <github:dmyersturnbull,orcid:0000-0003-3610-4808>"
        fixes = dict(
            name=self.name,
            version="0.1.0",
            description="A new project",
            authors=self.authors,
            maintainers=self.authors,
            license=self.license_name.full_name(),
            keywords=str(["a new", "python project"]),
            homepage="https://github.com/{}/{}".format(self.username, self.name),
            repository="https://github.com/{}/{}".format(self.username, self.name),
            documentation="https://{}.readthedocs.io".format(self.name),
            build="https://github.com/{}/{}/actions".format(self.username, self.name),
            issues="https://github.com/{}/{}/issues".format(self.username, self.name),
            source="https://github.com/{}/{}".format(self.username, self.name),
        )
        """
        fixes[author_line] = "\n".join(
            ['    "{} <github:...,orcid:...>"'.format(author) for author in self.authors]
        )
        """
        new_lines = self._set_lines(lines, fixes)
        # this one is fore tool.tyrannosaurus.sources
        # this is a hack
        new_lines = self._set_lines(new_lines, dict(maintainers=self.username))
        new_lines = [line for line in new_lines if "Douglas Myers-Turnbull" not in line]
        return new_lines

    def _set_lines(self, lines: Sequence[str], prefixes: Mapping[str, Union[int, str]]):
        new_lines = []
        set_val = set()
        for line in lines:
            new_line = line
            for key, value in prefixes.items():
                if isinstance(value, str):
                    value = '"' + value + '"'
                if line.startswith(key + " = ") and key not in set_val:
                    new_line = key + " = " + str(value)
                    set_val.add(key)
            new_lines.append(new_line)
        return new_lines


class _PyPiHelper:
    def __init__(self, timeout_sec: int = 10):
        self.timeout_sec = timeout_sec

    def new_versions(self, pkg_versions: Mapping[str, str]) -> Mapping[str, Tup[str, str]]:
        updated = {}
        for pkg, version in pkg_versions.items():
            try:
                new = self.get_version(pkg)
            except ValueError:
                logger.error("Did not find package {}".format(pkg), exc_info=True)
            else:
                if new != version:
                    updated[pkg] = version, new
        return updated

    def get_version(self, name: str):
        pat = re.compile(r"^[^(]+\(from versions: ([^)]+)+\).*$")
        # TODO this hangs when run in pytest
        proc = subprocess.Popen(
            ["pip", "install", name + "=="],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf8",
        )
        stdout, stderr = proc.communicate(timeout=self.timeout_sec)
        # result = subprocess.run(
        #    ["pip", "install", name + "=="],
        #    capture_output=True,
        #    encoding="utf8"
        # )
        text = pat.fullmatch(stderr).group(1).strip()
        if text == "none":
            raise ValueError("Failed to find package {}".format(name))
        return text.split(" ")[-1]


class _CondaForgeHelper:
    def has_pkg(self, name: str):
        # unfortunately, Anaconda returns 200 even if the page doesn't exist
        # TODO needed verify=False to get it working on CI
        try:
            r = requests.get("http://anaconda.org/conda-forge/{}".format(name), verify=False)
        except OSError:
            logger.error(
                "Failed fetching from anaconda.org. Assuming {} is in Conda-Forge.".format(name),
                exc_info=True,
            )
            return True
        return "login?next" not in r.url


class _EnvHelper:
    def process(self, name: str, deps, extras: bool) -> Sequence[str]:
        helper = _CondaForgeHelper()
        lines = [
            "# auto-generated by `tyrannosaurus env`",
            "name: " + name,
            "channels:",
            "    - conda-forge",
            "dependencies:",
        ]
        not_in = []
        for key, value in deps.items():
            # TODO
            if not isinstance(value, str):
                if value.get("optional") is True and not extras:
                    continue
                if "extras" in value:
                    logger.error("'extras' not supported for {} = {}".format(key, value))
                value = value.get("version")
            # TODO handle ~ correctly
            if "^" in value or "~" in value:
                match = re.compile(r"^[^~]([0-9]+)(?:\.([0-9]+))?(?:\.([0-9]+))?$").fullmatch(value)
                if match is not None:
                    value = (
                        ">="
                        + match.group(1)
                        + "."
                        + match.group(2)
                        + ",<"
                        + str(int(match.group(1)) + 1)
                        + ".0"
                    )
                else:
                    logger.error("Couldn't parse {}".format(key + " = =" + value))
            line = "    - " + key + value.replace(" ", "")
            if helper.has_pkg(key):
                lines.append(line)
            else:
                not_in.append(line)
        typer.echo("Found {} dependencies not in Conda-Forge.".format(len(not_in)))
        if len(not_in) > 0:
            lines.append("    - pip>=20")
            lines.append("    - pip:")
            for line in not_in:
                lines.append("    " + line)
        lines.append("")
        return lines


def _fast_scandir(topdir, trash):
    subdirs = [Path(f.path) for f in os.scandir(topdir) if Path(f).is_dir()]
    for dirname in list(subdirs):
        if (
            dirname.is_dir()
            and dirname.name
            not in {".tox", ".pytest_cache", ".git", ".idea", "docs", "__pycache__"}
            and dirname.name not in {str(s) for s in trash.get_list()}
        ):
            subdirs.extend(_fast_scandir(dirname, trash))
    return subdirs


__all__ = [
    "_TrashList",
    "_Env",
    "_License",
    "_InitTomlHelper",
    "_PyPiHelper",
    "_CondaForgeHelper",
    "_EnvHelper",
    "_fast_scandir",
]
