import click

from dsmr import __version__
from dsmr.dsmr import DSMRReader

@click.group()
@click.version_option(version=__version__)
def main():
    pass

@main.command()
def log():
    click.echo('log')

@main.command()
def read():
    clazz = DSMRReader()

    clazz.read()