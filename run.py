#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pwd
import contextlib
import subprocess
import click


@click.group(chain=True)
@click.option('--debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
def install_apt():
    """
    Install apt packages
    """
    click.echo('Install apt')


@cli.command()
def install_ruby():
    """
    Install Ruby gem packages
    """
    click.echo('Install ruby')


@cli.command()
def install_python():
    """
    Install Python packages
    """
    click.echo('Install python')


@cli.command()
def download():
    """
    Download packages
    """
    click.echo('Download packages')


@cli.command()
def setup_docker():
    """
    Set up Docker
    """
    click.echo('Set up Docker')


@cli.command()
def setup_git():
    """
    Set up git
    """
    click.echo('Set up git')


@cli.command()
def setup_tmuxinator():
    """
    Set up git
    """
    click.echo('Set up tmuxinator')


@cli.command()
def setup_vim_nox():
    """
    Set up vim nox
    """
    click.echo('Set up vim nox')


@cli.command()
def setup_zsh():
    """
    Set up zsh
    """
    click.echo('Set up zsh')


if __name__ == '__main__':
    cli(obj={})
