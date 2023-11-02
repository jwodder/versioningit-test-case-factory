This repository contains a program and a set of configurations & templates for
producing the test case archives used to test [versioningit][].  It probably
won't be of any use to you unless you like reading code for ad-hoc build
systems.

[versioningit]: https://github.com/jwodder/versioningit

Requirements
============

Beyond the Python requirements (documented in `pyproject.toml`), building the
test cases requires the following external programs:

- Git
- Mercurial
- `diff`
- `patch`
- `rsync`

Usage
=====

The entry point to the build system is the `factory` command, which can be run
in an isolated environment via [hatch][] by preceding commands with "`hatch
run`".

[hatch]: https://hatch.pypa.io

- `factory build` — Build the test cases

- `factory clean` — Remove the target & build directories produced by `factory
  build`

- `factory compare path/to/versioningit` — Compare the contents of the archive
  assets produced by a previous `factory build` call against the archives
  currently present in the given local clone of the [versioningit][] repository

- `factory deploy path/to/versioningit` — Replace the test case files in the
  given local clone of the [versioningit][] repository with those produced by a
  previous `factory build` call

Run the various commands with the `--help` option for more details.
