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

    if ctx.invoked_subcommand is None:
        ctx.invoke(download)

        ctx.invoke(install_apt)
        ctx.invoke(install_ruby)
        ctx.invoke(install_python)

        ctx.invoke(setup_docker)
        ctx.invoke(setup_git)
        ctx.invoke(setup_tmuxinator)
        ctx.invoke(setup_vim_nox)
        ctx.invoke(setup_zsh)


@cli.command()
@click.pass_context
def install_apt(ctx):
    """
    Install apt packages
    """
    click.echo('Install apt')

    s = ctx.obj['SETUPOBJ']

    s.apt_update()

    apt = config.install.get('apt', {})
    uninstall_packages = apt.get('uninstall', [])
    install_packages = apt.get('install', [])

    s.apt_uninstall(uninstall_packages)
    s.apt_install(install_packages)


@cli.command()
@click.pass_context
def install_ruby(ctx):
    """
    Install Ruby gem packages
    """
    click.echo('Install ruby')

    s = ctx.obj['SETUPOBJ']

    ruby = config.install.get('ruby', {})
    uninstall_packages = ruby.get('uninstall', [])
    install_packages = ruby.get('install', [])

    if uninstall_packages or install_packages:
        s.apt_install(['ruby'])

        s.gem_uninstall(uninstall_packages)
        s.gem_install(install_packages)


@cli.command()
@click.pass_context
def install_python(ctx):
    """
    Install Python packages
    """
    click.echo('Install python')

    s = ctx.obj['SETUPOBJ']

    py = config.install.get('python', {})
    uninstall_packages = py.get('uninstall', [])
    s.pip_uninstall(uninstall_packages)

    install = py.get('install', {})
    glb_install_packages = install.get('global', {})
    usr_install_packages = install.get('user', {})
    
    s.pip_install(glb_install_packages)
    s.pip_install(usr_install_packages, user=True)


@cli.command()
@click.pass_context
def download(ctx):
    """
    Download packages
    """
    click.echo('Download packages')

    s = ctx.obj['SETUPOBJ']

    s.apt_install(['curl'])

    dl = config.download or {}
    deb_packages = dl.get('deb', [])
    misc_packages = dl.get('misc', [])

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


@cli.command()
@click.pass_context
def setup_git(ctx):
    """
    Set up git
    """
    click.echo('Set up git')

    s = ctx.obj['SETUPOBJ']


@cli.command()
@click.pass_context
def setup_tmuxinator(ctx):
    """
    Set up git
    """
    click.echo('Set up tmuxinator')

    s = ctx.obj['SETUPOBJ']


@cli.command()
@click.pass_context
def setup_vim_nox(ctx):
    """
    Set up vim nox
    """
    click.echo('Set up vim nox')

    s = ctx.obj['SETUPOBJ']


@cli.command()
@click.pass_context
def setup_zsh(ctx):
    """
    Set up zsh
    """
    click.echo('Set up zsh')

    s = ctx.obj['SETUPOBJ']


class Setup:
    def __init__(self, debug):
        self.debug = debug

        self.home_dir = os.path.expanduser('~')

        self.apt_installed_packages = []
        self.ruby_installed_packages = []
        self.py_installed_packages = []
        self.downloaded_packages = []

    def _run(self, command):
        # return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return subprocess.run(command)

    def download_file(self, source, filename):
        target = os.path.join(self.home_dir, 'Downloads', filename)

        self._run(['curl', '-L', source, '--output', target])

        self.downloaded_packages.append(target)
        return target

    def apt_update(self):
        self._run(['sudo', 'apt-get', 'update'])

    def apt_install(self, packages):
        cmd = ['sudo', 'apt-get', '-f', '-y', 'install']
        cmd.extend(packages)
        self._run(cmd)

        self.apt_installed_packages.extend(packages)

    def apt_uninstall(self, packages):
        cmd = ['sudo', 'apt-get', 'remove']
        cmd.extend(packages)
        self._run(cmd)
        self.apt_cleanup()

    def apt_cleanup(self):
        self._run(['sudo', 'apt-get', '-y', 'autoremove'])
        self._run(['sudo', 'apt-get', '-y', 'clean'])
        self._run(['sudo', 'apt-get', '-y', 'autoclean'])

    def deb_install(self, package):
        self._run(['sudo', 'dpkg', '-i', package])

    def pip_uninstall(self, packages):
        cmd = ['sudo', 'pip3', 'uninstall', '--yes']
        cmd.extend(packages)
        self._run(cmd)

    def pip_install(self, packages, user=False):
        cmd = ['sudo', 'pip3', 'install', '--force-reinstall', '--progress-bar', 'pretty']

        if user:
            cmd.append('--user')

        for pkg, version in packages.items():
            if version == '*':
                version = ''

            pkg_w_version = '{}{}'.format(pkg, version)
            cmd.append(pkg_w_version)

            self.py_installed_packages.append(pkg)

        self._run(cmd)

    def gem_uninstall(self, packages):
        cmd = ['sudo', 'gem', 'uninstall']
        cmd.extend(packages)
        self._run(cmd)

    def gem_install(self, packages):
        cmd = ['sudo', 'gem', 'install']
        cmd.extend(packages)
        self._run(cmd)


if __name__ == '__main__':
    cli(obj={})
