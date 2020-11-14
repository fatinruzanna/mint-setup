#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pwd
import contextlib
import subprocess
import click
import config


@click.group(chain=True, invoke_without_command=True)
@click.option('--debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)

    s = Setup(debug)
    ctx.obj['SETUPOBJ'] = s

    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')

        ctx.invoke(download)

        ctx.invoke(install_apt)
        ctx.invoke(install_ruby)
        ctx.invoke(install_python)

        ctx.invoke(setup_docker)
        ctx.invoke(setup_git)
        ctx.invoke(setup_tmuxinator)
        ctx.invoke(setup_vim_nox)
        ctx.invoke(setup_zsh)
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)


@cli.command()
@click.pass_context
def install_apt(ctx):
    """
    Install apt packages
    """
    click.echo('Install apt')

    s = ctx.obj['SETUPOBJ']
    s.test()

    s.apt_update()

    apt = config.install.get('apt', {})
    uninstall_packages = apt.get('uninstall', [])
    install_packages = apt.get('install', [])

    s.apt_remove(uninstall_packages)
    s.apt_install(install_packages)


@cli.command()
@click.pass_context
def install_ruby(ctx):
    """
    Install Ruby gem packages
    """
    click.echo('Install ruby')

    s = ctx.obj['SETUPOBJ']
    s.test()


@cli.command()
@click.pass_context
def install_python(ctx):
    """
    Install Python packages
    """
    click.echo('Install python')

    s = ctx.obj['SETUPOBJ']
    s.test()


@cli.command()
@click.pass_context
def download(ctx):
    """
    Download packages
    """
    click.echo('Download packages')

    s = ctx.obj['SETUPOBJ']
    s.test()

    s.apt_install(['curl'])

    dl = config.download or {}
    deb_packages = dl.get('deb', [])
    misc_packages = dl.get('misc', [])

    click.echo('DEB packages = {}'.format(deb_packages))
    click.echo('MISC packages = {}'.format(misc_packages))

    for pkg in deb_packages:
        target = s.download_file(**pkg)
        s.deb_install(target)

    for pkg in misc_packages:
        s.download_file(**pkg)


@cli.command()
@click.pass_context
def setup_docker(ctx):
    """
    Set up Docker
    """
    click.echo('Set up Docker')

    s = ctx.obj['SETUPOBJ']
    s.test()


@cli.command()
@click.pass_context
def setup_git(ctx):
    """
    Set up git
    """
    click.echo('Set up git')

    s = ctx.obj['SETUPOBJ']
    s.test()


@cli.command()
@click.pass_context
def setup_tmuxinator(ctx):
    """
    Set up git
    """
    click.echo('Set up tmuxinator')

    s = ctx.obj['SETUPOBJ']
    s.test()


@cli.command()
@click.pass_context
def setup_vim_nox(ctx):
    """
    Set up vim nox
    """
    click.echo('Set up vim nox')

    s = ctx.obj['SETUPOBJ']
    s.test()


@cli.command()
@click.pass_context
def setup_zsh(ctx):
    """
    Set up zsh
    """
    click.echo('Set up zsh')

    s = ctx.obj['SETUPOBJ']
    s.test()


class Setup:
    def __init__(self, debug):
        self.debug = debug

        self.home_dir = os.path.expanduser('~')

        self.apt_installed_packages = []
        self.ruby_installed_packages = []
        self.py_installed_packages = []
        self.downloaded_packages = []

        self.counter = 0

        self.print_counter()

    def test(self):
        self.counter += 1
        self.print_counter()

    def print_counter(self):
        click.echo('Current counter value = {}'.format(self.counter))

    def _run(self, command):
        # return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return subprocess.run(command)

    def apt_update(self):
        self._run(['sudo', 'apt-get', 'update'])

    def apt_install(self, packages):
        cmd = ['sudo', 'apt-get', '-f', '-y', 'install']
        cmd.extend(packages)
        self._run(cmd)

        self.apt_installed_packages.extend(packages)

    def apt_remove(self, packages):
        cmd = ['sudo', 'apt-get', 'remove']
        cmd.extend(packages)
        self._run(cmd)
        self.apt_cleanup()

    def apt_cleanup(self):
        self._run(['sudo', 'apt-get', '-y', 'autoremove'])
        self._run(['sudo', 'apt-get', '-y', 'autoclean'])

    def deb_install(self, package):
        self._run(['sudo', 'dpkg', '-i', package])

    def download_file(self, source, filename):
        target = os.path.join(self.home_dir, 'Downloads', filename)

        self._run(['curl', '-L', source, '--output', target])

        self.downloaded_packages.append(target)
        return target


if __name__ == '__main__':
    cli(obj={})
