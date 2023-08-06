# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project attempts to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.6.1 2020-05-16

### Added
 - A license (MIT).

### Changed
 - Reduced the usage of shortcut imports to improve compatibility with clctools,
   see [clctools#4](https://bitbucket.org/creminslab/clctools/issues/4).

### Fixed
  - Minor bugs:
  [#77](https://bitbucket.org/creminslab/lib5c/issues/77),
  [#78](https://bitbucket.org/creminslab/lib5c/issues/78),
  [#50](https://bitbucket.org/creminslab/lib5c/issues/50),
  [#81](https://bitbucket.org/creminslab/lib5c/issues/81).

## 0.6.0 - 2020-03-11

This version finally brings Python 3 support to lib5c!

Currently all tests and all tutorials pass under both Python 2.7 and Python 3.6,
but it's possible that a few bugs exist in areas with low test coverage.

### Added
 - Experimental Python 3 support, see [#54](https://bitbucket.org/creminslab/lib5c/issues/54).
 - New functionality for getting data for the tutorials in
   `lib5c.util.demo_data`, see [#75](https://bitbucket.org/creminslab/lib5c/issues/75).
 - New utility function for loading config files using ConfigParser:
   `lib5c.util.config.parse_config()`.

### Changed
 - numpy arrays containing strings are now always created with a "U" dtype.

### Fixed
 - You can now pass a `(positions, labels)` tuple to the `xticks` and `yticks`
   kwargs of a function decorated with `@plotter`, see [#25](https://bitbucket.org/creminslab/lib5c/issues/25).
 - When running in Python 3 environments where ConfigParser is not available,
   the default pipeline config will have all its "%" symbols escaped when it is
   dropped to disk, see [#73](https://bitbucket.org/creminslab/lib5c/issues/73).
 - Y-axis gene tracks now appear correctly on trans heatmaps, see [#69](https://bitbucket.org/creminslab/lib5c/issues/69).
 - Two-way thresholding now works even when there is only one region, see [#71](https://bitbucket.org/creminslab/lib5c/issues/71).
 - Quoting paths with wildcards when passing them to lib5c commands no longer
   prevents glob expansion in Windows, see [#76](https://bitbucket.org/creminslab/lib5c/issues/76).

### Updates/maintenance
 - Bumped minimum `matplotlib` dependency, see [#59](https://bitbucket.org/creminslab/lib5c/issues/59).
 - Minor documentation improvements, see [#63](https://bitbucket.org/creminslab/lib5c/issues/63),
   [#64](https://bitbucket.org/creminslab/lib5c/issues/64),
   and [18a7f6](https://bitbucket.org/creminslab/lib5c/commits/18a7f6).
 - Changed testing/linting to use [tox](https://tox.readthedocs.io/en/latest/).
   tox now serves as a centralized place to control maintenance-related actions
   like running the tutorials, building Docker images, testing the doc build,
   etc.
 - Since tox doesn't support shell redirection/expansion, we moved the Docker
   one-liners into a new utility script `_docker.py` in the project root which
   is called by the new docker testenv (`tox -e docker`).
 - Overhauled doc build process. We now use [sphinxcontrib-apidoc](https://pypi.org/project/sphinxcontrib-apidoc/)
   to automatically run `sphinx-apidoc` on every doc build, avoiding the need to
   commit the per-module apidoc-generated .rst files to git. We also use the
   [readthedocs config file](https://docs.readthedocs.io/en/stable/config-file/v2.html)
   to configure the doc build on readthedocs. Both the local (`tox -e docs`) and
   readthedocs builds are now configured to exit when they encounter a warning.
 - Reduced the fragility of many doctest cases that relied on the ordering of
   dictionary keys.
 - Streamlined Docker image build so that building the wheel beforehand is no
   longer necessary, see [#67](https://bitbucket.org/creminslab/lib5c/issues/67).
   This also fixes [#68](https://bitbucket.org/creminslab/lib5c/issues/68).
 - We now use [setuptools-scm](https://pypi.org/project/setuptools-scm/) to
   manage version information instead of versioneer. We repurposed the existing
   `lib5c._version` module to provide setuptools-scm specific functionality.
 - Added dependency on configparser to make config file parsing more consistent
   across Python versions.
 - Relaxed maximum version constraint on python-daemon, since luigi seems to be
   handling this now.
 - Replaced references to pandas's deprecated `get_matrix()` bound method with
   the now-recommended `values` property.
 - Thanks to [#75](https://bitbucket.org/creminslab/lib5c/issues/75) and [#76](https://bitbucket.org/creminslab/lib5c/issues/76),
   tutorials have been updated to use `lib5c.util.demo_data` and now run on
   Windows (`tox -e tutorials`). Tutorials now run on Python 3.6.

## 0.5.5 - 2020-02-04

### Changed
 - Enabled extrapolation in `lib5c.util.lowess.lowess_fit()`, see [#60](https://bitbucket.org/creminslab/lib5c/issues/60).

### Updates/maintenance
 - Enforce maximum supported version of `statsmodels` since they are no longer building Python 2 wheels.

## 0.5.4 - 2019-06-07

First wave of major heatmap plotting upgrades plus streamlining of the release
process via Bitbucket Pipelines.

### Added
- A changelog, see [#47](https://bitbucket.org/creminslab/lib5c/issues/47).

### Changed
- ExtendableHeatmap ChIP-seq track and gene track plotting are now faster
  thanks to the use of PolyCollection and LineCollection, see [#28](https://bitbucket.org/creminslab/lib5c/issues/28).

### Fixed
- Bug [#56](https://bitbucket.org/creminslab/lib5c/issues/56).

### Updates/maintenance
- Updated `flake8` configuration (to match previous behavior when using latest
  version of `flake8`).
- Simplified `.gitignore`.
- Tests are now performed by Bitbucket Pipelines on every push.
- Reworked documentation to use [Read the Docs](https://readthedocs.org/).
- Moved tutorials to new `tutorials/` directory under project root.
- Tutorials are now built and published as an independent step in Bitbucket
  Pipelines, separate from the documentation build process.
- Deployment to PyPI and Docker Hub is now performed on tag push by Bitbucket
  Pipelines.

## 0.5.3 - 2018-10-15

First official release, corresponds to what was used in the final version of
[this paper](https://doi.org/10.1016/j.cels.2019.02.006).

## Diffs
- [0.6.1](https://bitbucket.org/creminslab/lib5c/branches/compare/0.6.1..0.6.0#diff)
- [0.6.0](https://bitbucket.org/creminslab/lib5c/branches/compare/0.6.0..0.5.5#diff)
- [0.5.5](https://bitbucket.org/creminslab/lib5c/branches/compare/0.5.5..0.5.4#diff)
- [0.5.4](https://bitbucket.org/creminslab/lib5c/branches/compare/0.5.4..0.5.3#diff)
- [0.5.3](https://bitbucket.org/creminslab/lib5c/src/0.5.3)
