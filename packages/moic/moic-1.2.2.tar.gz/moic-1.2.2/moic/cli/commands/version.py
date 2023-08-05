"""
Module which contains the version command for moic
"""
import click
import pkg_resources

from moic.cli import console


@click.command()
def version():
    """
    Provide the current moic installed version
    """
    console.print(f"Moic version: [green]{pkg_resources.get_distribution('moic').version}[/]")
