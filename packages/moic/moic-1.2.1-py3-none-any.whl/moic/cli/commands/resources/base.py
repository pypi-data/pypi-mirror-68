"""
Module for base Moic resources commands
"""
import click

from moic.cli import console, global_settings
from moic.cli.utils import get_plugin_command


# List Commands
# TODO: Add autocomplete on all commands
@click.group()
def resources():
    """List projects, issue_types, priorities, status"""
    if not global_settings.get("current_context"):
        console.print("[yellow]No context defined yet[/yellow]")
        console.print("[grey]> Please run '[bold]moic context add[/bold]' to setup configuration[/grey]")
        console.line()
        exit(0)


@resources.command()
def projects():
    """
    List projects
    """
    get_plugin_command("resources", "projects")()


@resources.command()
def issue_type():
    """
    List issue types
    """
    get_plugin_command("resources", "issue_type")()


@resources.command()
def priorities():
    """
    List priorities
    """
    get_plugin_command("resources", "priorities")()


@resources.command()
def status():
    """
    List status
    """
    get_plugin_command("resources", "status")()
