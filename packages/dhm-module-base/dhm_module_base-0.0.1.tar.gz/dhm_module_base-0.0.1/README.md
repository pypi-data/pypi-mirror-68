# DHM Base Module

Basic module which uses software principles used in the repository "surfclass".
Build status: [![CircleCI](https://circleci.com/gh/Kortforsyningen/dhm-module-base.svg?style=svg)](https://circleci.com/gh/Kortforsyningen/dhm-module-base)

This is a basis module, meant as a "mother" module for internal tasks in SDFE. Functionality with general purposes, including configuration files and settings
can be implemented here. Specialised functionality is sought to be implemented in "plugins". Plugins can be developed in separate repositories with this module as dependency, how to do that will be explained in a later section.
An example of a plugin that has this module as a dependency is described here: https://github.com/Kortforsyningen/dhm-module-example

The CLI module is based on Click https://click.palletsprojects.com/en/7.x/

## Installation

### Conda Environment

```
git clone https://github.com/Kortforsyningen/dhm-module-base
cd dhm-module-base
conda env create -n dhm_module_base -f environment.yml
conda activate dhm_module_base
pip install .
```

The plugin can also be installed in developer or "editable" mode.

```
git clone https://github.com/Kortforsyningen/dhm-module-base
cd dhm-module-base
conda env create -n dhm_module_base -f environment-dev.yml
conda activate dhm_module_base
pip install -e .
```

## Using the plugin

The module installs itself as a python module, which registers an entry point that can be called on the commandline.
This module does not provide any commands itself, but allows plugins to register commands using a special entry point called `plugins`
Calling the module from the commandline yields: `dhm_module_base`

```
Usage: dhm_module_base [OPTIONS] COMMAND [ARGS]...

  dhm_module_base command line interface.

Options:
  --version                       Show the version and exit.
  -v, --verbosity [CRITICAL|ERROR|WARNING|INFO|DEBUG]
                                  Set verbosity level
  --help                          Show this message and exit.

Commands:
```

Note that the commands list is empty, as no plugins are registered.

## Repository structure

```
📦dhm-module-base
┣ 📂.circleci
┃ ┗ 📜config.yml # CircleCI setup with status checks
┣ 📂.vscode
┃ ┗ 📜settings.json # .vscode settings, added to .gitignore
┣ 📂src
┃ ┣ 📂dhm_module_base # the module installed by setup.py
┃ ┃ ┣ 📜__init.py__ # __init__.py marks the folder as a python module
┃ ┃ ┣ 📜cli.py # Click commandline
┃ ┃ ┣ 📜helpers.py # Helping functions such as logging
┃ ┃ ┣ 📜options.py # Custom Click options
┃ ┃ ┣ 📜settings.py # Configuration files and common settings importable by plugins
┣ 📂tests
┃ ┣ 📜conftest.py # Pytest configuration objects and fixtures
┃ ┗ 📜test_cli.py # Example pytest that checks that the commandline works
┣ 📜.gitignore
┣ 📜environment-dev.yml
┣ 📜environment.yml
┣ 📜LICENSE
┣ 📜README.md
┣ 📜setup.cfg # Contains repository specific rules regarding linting and docstrings
┗ 📜setup.py # setup.py contains metadata and entry points for the module.
```

### `setup.py`

`setup.py` is a special python file that describes how the module in `src` should be installed.
Vi have told python that `src\dhm_module_base` is a module, since it has an `__init__.py` file.
The commandline is registered as an entrypoint using `ENTRY_POINTS`.
Here we describe that this module has one entry point, which is `dhm_module_base`. This ensures we can call the
module from the commandline, as an example: `dhm_module_base --version`

```
ENTRY_POINTS = """
      [console_scripts]
      dhm_module_base=dhm_module_base.cli:cli
"""

```

### `with_plugins` register plugins

In `cli.py` we register a `click.group` and then tell click that this groups should take plugins using the decorator
`@with_plugins`.

```
@with_plugins(iter_entry_points("dhm_module_base.plugins"))
@click.group("dhm_module_base")
```

`iter_entry_points("dhm_module_base.plugins")` is the entry point plugins register commands to in their `setup.py`
Plugins now register their commands into the mother module by adding them to the `ENTRY_POINTS` section of their setup.py

```
ENTRY_POINTS = """
      [dhm_module_base.plugins]
      inout=dhm_module_example.core:inout
      pipe=dhm_module_example.core:pipe
"""
```

If the plugin can be loaded without errors, they will be automatically added to the mother module, under commands

```
dhm_module_base

Options:
  --version                       Show the version and exit.
  -v, --verbosity [CRITICAL|ERROR|WARNING|INFO|DEBUG]
                                  Set verbosity level
  --help                          Show this message and exit.

Commands:
  inout  Example command inout.
  pipe   Example of a custom options handler being used along with a...
```

`inout` and `pipe` are commands from a plugin using the `[dhm_module_base.plugins]` entry point to register itself to the click group in the mother module.
See example: https://github.com/Kortforsyningen/dhm-module-example/blob/master/setup.py#L38

# Github and CircleCI setup for existing python projects

Existing python projects should use the same repository structure as this one, with one (or more) modules in `src`.
Modules are registered if they have an `__init__.py` file inside. Repositories should also include a `tests` folder and a `setup.py` file.

## Pytest

Pytest https://docs.pytest.org/en/latest/

Pytest kan be used to write small or complex tests for internal classes and for the CLI itself.
For examples of how to use Pytest see https://github.com/Kortforsyningen/surfclass and https://github.com/Kortforsyningen/dhm-module-example
It is advised to test every command at the CLI level as a minimum.

Pytest should be set to run in `.circleci\config.yml` after every commit.

## Black formatting

Black https://black.readthedocs.io/en/stable/

Black is an automatic code formatter, that can be set up in Visual Studio Code or be called on the commandline.
using `black src`. If the formatting is good, an output like this is shown:

```
$: black src

All done! ✨ � ✨
4 files left unchanged.
```

Black can be installed using `pip install black` and is also included in the conda environment for this project, and
also in the circleCI check.

## Pydocstyle

Pydocstyle https://github.com/PyCQA/pydocstyle/ is a docstring module that helps ensure all public methods are properly documented.
In this repository docstrings are set to the `google` convention https://google.github.io/styleguide/pyguide.html#381-docstrings.

## CircleCI

CircleCI is setup in this repository with one job `- lint_test_py37_conda` which checks
the source code for the following things:

- Pylint,
- Black formatting,
- Pydocstyle,
- Pytest - unittest

If any of these tasks fail, commits are not allowed to be pushed to the master branch. It is advised that the master branch
is protected and that code can only be pushed to branches first, and then merged into master using a reviewer and code check. The
CircleCI setup can be extended to also push modules to PyPi using releases or tagged commits.
