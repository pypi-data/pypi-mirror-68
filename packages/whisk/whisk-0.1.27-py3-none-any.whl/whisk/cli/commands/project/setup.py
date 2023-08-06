import click
from whisk.project import Project
import whisk.git as git
import os
import subprocess

NOTEBOOK_EXAMPLE_PATH = "notebooks/getting_started.ipynb"

# A similar function is in utils, but pip install -e . hasn't been executed yet so it isn't available.
def has_unstaged_changes():
    res=subprocess.check_output("git status --porcelain",shell=True, universal_newlines=True)
    return ("\n" in res)

def exec(desc,cmd):
    """
    Executes the `cmd`, and prints `desc` prior to execution.
    If the exit code is nonzero, raises a `SystemExit` execption.
    """
    print(desc+"...", end="", flush=True)
    exit_code = subprocess.call(cmd, shell=True)
    if exit_code == 0:
        print("✓")
    else:
        print("⚠️  (exit code= {})".format(exit_code))
        raise SystemExit("💣 Aborting install. An error occurred running the install script.")

def exec_setup(nbenv):
    exec("Setting up venv","python3 -m venv {}/venv".format(os.getcwd()))
    exec("Installing Python dependencies via pip","venv/bin/pip install -r requirements.txt > /dev/null")
    print("Initializing the Git repo")
    # Idempotent so just execute
    os.system("git init > /dev/null 2>&1")
    # Would rather use --sys-prefix, but not working:
    # https://github.com/jupyter/notebook/issues/4567
    exec("Setting up venv={} for Jupyter Notebooks".format(nbenv),"venv/bin/python -m ipykernel install --user --name={}".format(nbenv))
    set_example_notebook_kernel(nbenv)
    # direnv will fail if not installed
    os.system("cp .envrc.example .envrc")
    os.system("direnv allow . > /dev/null 2>&1")
    if git.has_unstaged_changes():
        exec("Adding files to git", "git add .")
        exec("Making initial Git commit", "git commit -m 'Initial project structure' --author=\"Whisk <whisk@whisk-ml.org>\" > /dev/null")

def set_example_notebook_kernel(nbenv):
    # Read in the file
    with open(NOTEBOOK_EXAMPLE_PATH, 'r') as file :
      filedata = file.read()

    # This could be run after the initial cookiecutter install.
    filedata = filedata.replace("{{cookiecutter.project_name}}", nbenv)

    # Write the file out again
    with open(NOTEBOOK_EXAMPLE_PATH, 'w') as file:
        file.write(filedata)

@click.command()
def cli():
    """
    Sets up the project environment.
    This is called by default after :func:`whisk.whisk.create` and should be run manually after cloning an existing project.

    Setup performs the following actions:

    * Creates a `Python3 venv <https://docs.python.org/3/library/venv.html />`_ named "venv"
    * Installs the dependencies listed in the project's requirements.txt.
    * Initializes a Git repo
    * Creates an iPython kernel for use in Jupyter notebooks with name = <project_name>.
    * Creates a ``.envrc`` file based on ``.envrc.example`` for use with `direnv <https://github.com/direnv/direnv />`_.
      direnv loads environment variables listed in ``.envrc`` into the shell and is also used to auto-activate and
      deactivate the venv when entering and exiting the project directory.
    * Calls ``direnv allow .`` so the ``.envrc`` file can be loaded.
    * Makes an initial Git commit
    """
    nbenv = Project().name
    exec_setup(nbenv)
    print("Install completed ✓.")
