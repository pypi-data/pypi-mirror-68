"""Main module."""
import whisk
from cookiecutter.main import cookiecutter
import os
from os.path import dirname, realpath
# https://docs.python.org/3/library/pathlib.html
# Object-oriented filesystem paths
from pathlib import Path

def root_module_dir():
    """
    Returns a Path object with the root whisk module directory.
    """
    filepath = realpath(__file__)
    return Path(filepath).parents[0]

def cookiecutter_template_dir():
    return str(root_module_dir() / 'template/')

def create(project_name, output_dir=".", setup=None, force=False):
    """
    Creates a whisk project.

    Parameters
    ----------
    project_name : str
        Name of the directory to create for the project.

    output_dir : str, optional
        Path to create the directory. Default is the current working directory.

    setup : bool, optional
        Whether to run the post-creation setup command. By default this is `True`. If `False`, only the directory structure is created.

    force : bool, optional
        Recreates the project directory if it exists. Default is `False`.
    """
    # Locks to a specific version as earlier and later versions of whisk could expect a different
    # template structure.
    whisk_version = "whisk=={}".format(whisk.__version__)
    # `whisk_dependency` is more flexible (for example, specifying a local install)
    # than `whisk_install_requires` and is used in testing to require the local version of whisk.
    extra_content = {
        "project_name": project_name,
        # Added to the project's requirements.txt
        "whisk_dependency": whisk_version,
        # Added to the project's setup.py file
        "whisk_install_requires": whisk_version
    }
    if setup is not None:
        extra_content["setup"] = setup
    cookiecutter(cookiecutter_template_dir(),
                no_input=True,
                overwrite_if_exists=force,
                output_dir=output_dir,
                extra_context=extra_content)
