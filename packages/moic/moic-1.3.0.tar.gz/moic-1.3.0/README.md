# MOIC : My Own Issue CLI

> Freely inspired by https://pypi.org/project/jira-cli/

Command line utility to interact with issue manager such as Jira

## Getting Started

* Install moic
```bash
> pip install moic
```

* Configure moic
```bash
> moic configure
```

* Commands
```bash
> moic
Usage: moic [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  config    Configure Jira cli, setting up instance, credentials etc...
  issue     Create, edit, list Jira issues
  list      List projects, issue_types, priorities, status
  rabbit    Print an amazing rabbit: Tribute to @fattibenji...
  sprint    Create, edit, list Jira Sprints
  template  List, edit templates
  version   Provide the current moic installed version
```

## Autocompletion

To activate bash autocompletion just add:
* For bash
```
# In your .bashrc
eval "$(_MOIC_COMPLETE=source_bash moic)"
```
* For zsh
```
# In your .zshrc
eval "$(_MOIC_COMPLETE=source_zsh moic)"
```

## Contribute

Feel free [open issues on Gitlab](https://gitlab.com/brice.santus/moic/-/issues) or propose Merge Requests

### Prerequisites

This project is based on [Poetry](https://python-poetry.org/docs/) as a package manager. It allows the use of virtual environments and the lock of package versions, whether they are in your dependencies or just sub-dependencies of these dependencies.

### Setup

* Create virtualenv (Optionnaly you can use [pyenv](https://github.com/pyenv/pyenv) which is a Python Virtualenv Manager in combination with **Poetry**)
```bash
poetry shell
```
* Install dependencies
```bash
poetry install
```
* Install pre-commit (using [Pre-commit framework](https://pre-commit.com/))
```bash
pre-commit install
```
> Pre-commit will check isort, black, flake8

### Commit messages

This project uses semantic versioning so it is important to follow the rules of [conventional commits](https://www.conventionalcommits.org/).
