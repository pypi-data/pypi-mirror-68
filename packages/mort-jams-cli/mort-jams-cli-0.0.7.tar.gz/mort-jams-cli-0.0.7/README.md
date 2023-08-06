# Prodigy Teams CLI

The Command Line Interface program for **Prodigy Teams**.

## Prerequisites

Before using Prodigy Teams CLI you need to have a **Prodigy Teams** account.

You also need a deployed broker cluster.

You will also need Python 3.6+ in your system.

## Install

Make sure you have a Python version 3.6 or above:

```console
$ python --version

# or

$ python3.6 --version

# or

$ python3.7 --version

# etc
```

Install with Python (using the same `python` version 3.6 or above, as selected above):

```console
$ python -m pip install prodigy-teams-cli
```

Then in your terminal you will have a `prodigyteams` program/command:

```console
$ prodigyteams --help

Usage: prodigyteams [OPTIONS] COMMAND [ARGS]...

  Prodigy Teams Command Line Interface.

  More info at https://prodi.gy/

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  login     Login to your Prodigy Teams.
  packages  Sub-commands to interact with packages (including models).
  projects  Sub-commands to interact with projects.
  sources   Sub-commands for sources.
  tasks     Sub-commands to interact with tasks.
```

If you want to have completion in your terminal (for Bash, Zsh, Fish, or PowerShell) run:

```console
$ prodigyteams --install-completion

bash completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

After that, re-start your terminal, and you will have completion for all the subcommands and options when you hit <kbd>TAB</kbd>.

## Extensive docs

## `prodigyteams`

Prodigy Teams Command Line Interface.

More info at https://prodi.gy/

**Usage**:

```console
$ prodigyteams [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Print version and exit.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `login`: Login to your Prodigy Teams.
* `packages`: Sub-commands to interact with packages...
* `projects`: Sub-commands to interact with projects.
* `sources`: Sub-commands for sources.
* `tasks`: Sub-commands to interact with tasks.

## `prodigyteams login`

Login to your Prodigy Teams.

You normally don't need to call this manually.
It will automatically authenticate when needed.

**Usage**:

```console
$ prodigyteams login [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `prodigyteams packages`

Sub-commands to interact with packages (including models).

**Usage**:

```console
$ prodigyteams packages [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Add a package from the local filesystem.
* `delete`: Delete a package.
* `download`: Download a package to the current directory.
* `list`: List all the packages including built-ins.
* `list-package`: List all the binary files for a package.

### `prodigyteams packages add`

Add a package from the local filesystem.

It should be a valid file in your local file system,
it will also be validated and indexed by your broker's Python Package Index.

**Usage**:

```console
$ prodigyteams packages add [OPTIONS] PACKAGE
```

**Options**:

* `--allowoverwrite / --no-allowoverwrite`
* `--help`: Show this message and exit.

### `prodigyteams packages delete`

Delete a package.

**Usage**:

```console
$ prodigyteams packages delete [OPTIONS] PACKAGE
```

**Options**:

* `--force / --no-force`: Force deletion without confirmation
* `--help`: Show this message and exit.

### `prodigyteams packages download`

Download a package to the current directory.

**Usage**:

```console
$ prodigyteams packages download [OPTIONS] PACKAGE FILENAME
```

**Options**:

* `--help`: Show this message and exit.

### `prodigyteams packages list`

List all the packages including built-ins.

**Usage**:

```console
$ prodigyteams packages list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `prodigyteams packages list-package`

List all the binary files for a package.

**Usage**:

```console
$ prodigyteams packages list-package [OPTIONS] PACKAGE
```

**Options**:

* `--help`: Show this message and exit.

## `prodigyteams projects`

Sub-commands to interact with projects.

**Usage**:

```console
$ prodigyteams projects [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List all the projects.

### `prodigyteams projects list`

List all the projects.

**Usage**:

```console
$ prodigyteams projects list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `prodigyteams sources`

Sub-commands for sources.

**Usage**:

```console
$ prodigyteams sources [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Add a source from local filesystem.
* `delete`: Delete a source.
* `list`: List all the sources.

### `prodigyteams sources add`

Add a source from local filesystem.

It should be a valid file in your local system,
it will be uploaded to your cluster.

**Usage**:

```console
$ prodigyteams sources add [OPTIONS] SOURCE
```

**Options**:

* `--allowoverwrite / --no-allowoverwrite`
* `--help`: Show this message and exit.

### `prodigyteams sources delete`

Delete a source.

**Usage**:

```console
$ prodigyteams sources delete [OPTIONS] SOURCE
```

**Options**:

* `--force / --no-force`: Force deletion without confirmation
* `--help`: Show this message and exit.

### `prodigyteams sources list`

List all the sources.

**Usage**:

```console
$ prodigyteams sources list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `prodigyteams tasks`

Sub-commands to interact with tasks.

**Usage**:

```console
$ prodigyteams tasks [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List all the tasks.

### `prodigyteams tasks list`

List all the tasks.

**Usage**:

```console
$ prodigyteams tasks list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
