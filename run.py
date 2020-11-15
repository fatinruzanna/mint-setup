#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pwd
import contextlib
import subprocess
import click
import config

SHELL_BASH = 'bash'
SHELL_ZSH = 'zsh'


GIT_APT_PACKAGES = ['git', 'gitk', 'meld']
GIT_DOT_SHRC = 'git/bashrc'
GIT_DOT_GITCONFIG = 'git/gitconfig'

ZSH_APT_PACKAGE = 'zsh'
ZSH_DOT_ZSHRC = 'zsh/zshrc'


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
        s.apt_install(['ruby', 'ruby-dev'])

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

    git = config.setup.get('git', {})
    enabled = git.get('enable', False)
    if not enabled:
        return

    cfg = git.get('config', {})
    s.setup_git(cfg)



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

    zsh = config.setup.get('zsh', {})
    enabled = zsh.get('enable', False)
    if not enabled:
        return

    cfg = zsh.get('config', {})
    s.setup_zsh(cfg)


class Setup:
    def __init__(self, debug):
        self.debug = debug

        self.home_dir = os.path.expanduser('~')
        self.user = pwd.getpwuid(os.getuid())[0]

        self.apt_installed_packages = []
        self.ruby_installed_packages = []
        self.py_installed_packages = []
        self.downloaded_packages = []

        self.setup_summary = []

    def download_file(self, source, filename):
        if not source and not filename:
            return

        target = os.path.join(self.home_dir, 'Downloads', filename)

        self._run(['curl', '-L', source, '--output', target])

        self.downloaded_packages.append(target)
        return target

    def apt_update(self):
        self._run(['sudo', 'apt-get', 'update'])

    def apt_install(self, packages):
        if not packages:
            return

        cmd = ['sudo', 'apt-get', '-f', '-y', 'install']
        cmd.extend(packages)
        self._run(cmd)

        self.apt_installed_packages.extend(packages)

    def apt_uninstall(self, packages):
        if not packages:
            return

        cmd = ['sudo', 'apt-get', 'remove']
        cmd.extend(packages)
        self._run(cmd)
        self.apt_cleanup()

    def apt_cleanup(self):
        self._run(['sudo', 'apt-get', '-y', 'autoremove'])
        self._run(['sudo', 'apt-get', '-y', 'clean'])
        self._run(['sudo', 'apt-get', '-y', 'autoclean'])

    def deb_install(self, package):
        if not package:
            return

        self._run(['sudo', 'dpkg', '-i', package])

    def pip_uninstall(self, packages):
        if not packages:
            return

        cmd = ['sudo', 'pip3', 'uninstall', '--yes']
        cmd.extend(packages)
        self._run(cmd)

    def pip_install(self, packages, user=False):
        if not packages:
            return

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
        if not packages:
            return

        cmd = ['sudo', 'gem', 'uninstall']
        cmd.extend(packages)
        self._run(cmd)

    def gem_install(self, packages):
        if not packages:
            return

        cmd = ['sudo', 'gem', 'install']
        cmd.extend(packages)
        self._run(cmd)

    def setup_git(self, cfg):
        self.apt_install(GIT_APT_PACKAGES)

        dot_gitconfig = os.path.join(self.home_dir, '.gitconfig')
        self._run(['cp', GIT_DOT_GITCONFIG, dot_gitconfig])

        name = cfg.get('name')
        email = cfg.get('email')

        if name:
            self._run(['git', 'config', '--global', 'user.name', '"%s"' % name])

        if email:
            self._run(['git', 'config', '--global', 'user.email', '"%s"' % email])

        # TODO: Check version!!! Below is for >= 1.7.9:
        # self._run(['git', 'config', '--global pull.rebase', 'true'])
        # TODO: Check version!!! Below is for < 1.7.9:
        # self._run(['git', 'config', '--global branch.autosetuprebase', 'always'])

        self._add_to_setup_summary('Git config file: %s' % dot_gitconfig)

        if cfg.get('set_up_bash'):
            local_git_repo = os.path.join(self.home_dir, '.git')
            git_bin_dir = os.path.join(self.home_dir, 'bin/git')
            if not os.path.exists(local_git_repo):
                self._run(['git', 'clone', 'git://git.kernel.org/pub/scm/git/git.git', local_git_repo])

            self._run(['mkdir', '-p', git_bin_dir])
            self._run(['cp', '%s/contrib/completion/git-completion.bash' % local_git_repo, '%s/git-completion.sh' % git_bin_dir])
            self._run(['chmod', 'u+x', '%s/git-completion.sh' % git_bin_dir])
            self._run(['rm', '-rf', local_git_repo])

            settings_file = self._setup_bashrc()
            self._add_to_shell_settings(settings_file, GIT_DOT_SHRC)

            self._add_to_setup_summary('Git completion and terminal prompt configured: %s' % settings_file)

    def setup_zsh(self, cfg):
        settings_file = self._setup_zshrc()
        self.apt_install([ZSH_APT_PACKAGE])

        self._run(['sudo', 'chsh', '-s', '$(which zsh)', self.user])
        
        ohmyzsh_repo = os.path.join(self.home_dir, '.oh-my-zsh')
        if not os.path.exists(ohmyzsh_repo):
            self._run(['git', 'clone', 'git://github.com/robbyrussell/oh-my-zsh.git', ohmyzsh_repo])

        self._add_to_shell_settings(settings_file, ZSH_DOT_ZSHRC, source_file=False)

        self._add_to_setup_summary('oh-my-zsh repository: %s' % ohmyzsh_repo)

    def _run(self, command):
        # return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return subprocess.run(command)

    def _setup_bashrc(self):
        return self._setup_shell_settings(SHELL_BASH)

    def _setup_zshrc(self):
        return self._setup_shell_settings(SHELL_ZSH)

    def _get_shell_settings_path(self, shell):
        if shell == SHELL_BASH:
            settings_file = '.bashrc'
        elif shell == SHELL_ZSH:
            settings_file = '.zshrc'
        else:
            RuntimeError('Unknown shell: {}'.format(shell))

        return os.path.join(self.home_dir, settings_file)

    def _setup_shell_settings(self, shell):
        settings_file = self._get_shell_settings_path(shell)

        if not os.path.exists(settings_file):
            self._run(['touch', settings_file])

        return settings_file

    def _add_to_shell_settings(self, shell_file, settings_file, source_file=True):
        with open(settings_file, 'r') as f:
            data = f.read()

        with open(shell_file, 'a') as f:
            f.write(data)

        if source_file:
            self._run(['bash', '-c', 'source', shell_file])


    def _add_to_setup_summary(self, log):
        if isinstance(log, str):
            self.setup_summary.append(log)



if __name__ == '__main__':
    cli(obj={})
