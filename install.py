import os
import contextlib
import shlex
import subprocess
import logging
import json


GIT_APT_PACKAGE = 'git'
GIT_DOT_SHRC = 'git/bashrc'
GIT_DOT_GITCONFIG = 'git/gitconfig'

ZSH_APT_PACKAGE = 'zsh'
ZSH_DOT_ZSHRC = 'zsh/zshrc'

TMUX_APT_PACKAGE = 'tmux'
TMUX_DOT_TMUXCONF = 'tmux/tmuxconf'

VIM_APT_PACKAGES_REMOVE = [
    'vim',
    'vim-runtime',
    'gvim',
    'vim-tiny',
    'vim-common',
    'vim-gui-common',
]
VIM_APT_PACKAGE = 'vim-nox'
VIM_DOT_SHRC = 'vim/bashrc'
VIM_DOT_VIMRC = 'vim/vimrc'

PYTHON_VIRTUALENV_PIP_PACKAGE = 'virtualenv'
PYTHON_VIRTUALENVWRAPPER_PIP_PACKAGE = 'virtualenvwrapper'
PYTHON_DOT_SHRC = 'python/bashrc'

NODEJS_APT_PACKAGE = 'nodejs'
NODEJS_DOT_SHRC = 'javascript/bashrc'

LOG_NAME = 'install'
LOG_FILENAME = '%s.log' % LOG_NAME
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s - [%(levelname)-8s] - %(message)s'
LOG_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

DEFAULT_APT_INSTALL = [
    'build-essential',
    'wget',
]


def main():
    with open("settings.json") as f:
        config = json.load(f)

    setup = Setup(config)
    setup.run()


class Setup():

    def __init__(self, config):
        self.config = config
        self.log = self._logger()
        self.apt_installed_packages = []
        self.gem_installed_packages = []
        self.pip_installed_packages = []
        self.git_directory = None
        self.shell_settings = None
        self.home_dir = os.path.expanduser('~')


    def run(self):

        # installation packages
        self._run_apt()
        self._run_gem()
        self._run_pip()
        self._run_wget()

        # setup packages
        setup_config = self.config.get('setup')
        if not setup_config:
            return

        self._setup_shell_settings(setup_config)
        self._setup_git(setup_config)
        self._setup_zsh(setup_config)
        self._setup_tmux(setup_config)
        self._setup_vim(setup_config)
        self._setup_python(setup_config)
        self._setup_nodejs(setup_config)

        # clean up
        self._clean_up()


    def _run_apt(self):
        apt_config = self.config.get('apt')
        if not apt_config:
            return

        uninstall_packages = self._get_packages_from_list(apt_config, 'remove')
        install_packages = self._get_packages_from_list(apt_config, 'install', default_list=DEFAULT_APT_INSTALL)

        self.log.debug('Uninstalling and installing apt packages')

        if uninstall_packages or install_packages:
            self._system_run('sudo apt-get update')

        if uninstall_packages:
            self._system_run('sudo apt-get remove -y %s' % uninstall_packages)

        if install_packages:
            self._system_run('sudo apt-get install -y -f %s' % install_packages)

        self.apt_installed_packages = install_packages.split()


    def _run_gem(self):
        gem_config = self.config.get('gem')
        if not gem_config:
            return

        uninstall_packages = self._get_packages_from_list(gem_config, 'uninstall')
        install_packages = self._get_packages_from_list(gem_config, 'install')

        self.log.debug('Uninstalling and installing gem packages')

        if uninstall_packages or install_packages:
            self._system_run('sudo apt-get install -y -f rubygems')

        if uninstall_packages:
            self._system_run('sudo gem uninstall %s' % uninstall_packages)

        if install_packages:
            self._system_run('sudo gem install %s' % install_packages)

        self.gem_installed_packages = install_packages.split()


    def _run_pip(self):
        pip_config = self.config.get('pip')
        if not pip_config:
            return

        uninstall_packages = self._get_packages_from_list(pip_config, 'uninstall')
        install_packages = self._get_packages_from_list(pip_config, 'install')

        if uninstall_packages or install_packages:
            self._system_run('sudo easy_install pip')

        if uninstall_packages:
            self._system_run('sudo pip uninstall %s' % uninstall_packages)

        if install_packages:
            self._system_run('sudo pip install %s' % install_packages)

        self.pip_installed_packages = install_packages.split()


    def _run_wget(self):
        wget_config = self.config.get('wget')
        if not wget_config:
            return

        home_download_directory = os.path.join(self.home_dir, 'Downloads')
        download_packages = wget_config.get('download')
        if download_packages:
            self._system_run('sudo apt-get install -y -f wget')

        for package in download_packages:
            self._system_run('wget -P %s %s' % (home_download_directory, package))


    def _setup_shell_settings(self, setup_config):
        setup_zsh = setup_config.get('zsh')
        if not setup_zsh:
            return

        if not setup_zsh:
            settings_file = '.bashrc'
        else:
            settings_file = '.zshrc'

        home_settings_file = os.path.join(self.home_dir, settings_file)
        self.shell_settings = home_settings_file
        self._system_run('touch %s' % home_settings_file)


    def _setup_git(self, setup_config):
        git_config = setup_config.get('git')
        if not git_config:
            return

        directory = git_config.get('directory')
        if directory:
            self.git_directory = directory
            self._system_run('mkdir -p %s' % directory)

        name = git_config.get('name')
        email = git_config.get('email')

        if not name and not email:
            return

        if GIT_APT_PACKAGE not in self.apt_installed_packages:
            self._system_run('sudo apt-get install -y -f %s' % GIT_APT_PACKAGE)

        home_dot_gitconfig = os.path.join(self.home_dir, '.gitconfig')
        self._system_run('cp %s %s' % (GIT_DOT_GITCONFIG, home_dot_gitconfig))

        if name:
            self._system_run('git config --global user.name "%s"' % name)

        if email:
            self._system_run('git config --global user.email "%s"' % email)

        # TODO: Check version!!! Below is for >= 1.7.9:
        # self._system_run('git config --global pull.rebase true')
        # TODO: Check version!!! Below is for < 1.7.9:
        # self._system_run('git config --global branch.autosetuprebase always')

        if 'bashrc' in self.shell_settings:
            local_git_repo = os.path.join(self.home_dir, '.git')
            git_bin_dir = os.path.join(self.home_dir, 'bin/git')
            self._system_run('git clone git://git.kernel.org/pub/scm/git/git.git %s' % local_git_repo)
            self._system_run('mkdir -p %s' % git_bin_dir)
            self._system_run('cp %s/contrib/completion/git-completion.bash %s/git-completion.sh' % (local_git_repo, git_bin_dir))
            self._system_run('chmod u+x %s/git-completion.sh' % git_bin_dir)
            self._system_run('rm -rf %s' % local_git_repo)
            self._add_to_shell_settings(GIT_DOT_SHRC)


    def _setup_zsh(self, setup_config):
        zsh_config = setup_config.get('zsh')
        if not zsh_config:
            return

        # TODO: Detect from dpkg-query -l zsh
        if ZSH_APT_PACKAGE not in self.apt_installed_packages:
            self._system_run('sudo apt-get install -y -f %s' % ZSH_APT_PACKAGE)

        self._system_run('sudo chsh -s /bin/zsh')

        home_ohmyzsh_repo = os.path.join(self.home_dir, '.oh-my-zsh')
        self._system_run('git clone git://github.com/robbyrussell/oh-my-zsh.git %s' % home_ohmyzsh_repo)

        self._add_to_shell_settings(ZSH_DOT_ZSHRC)


    def _setup_tmux(self, setup_config):
        tmux_config = setup_config.get('tmux')
        if not tmux_config:
            return

        # TODO: Detect from dpkg-query -l tmux
        if TMUX_APT_PACKAGE not in self.apt_installed_packages:
            self._system_run('sudo apt-get install -y -f %s' % TMUX_APT_PACKAGE)

        home_tmux_conf = os.path.join(self.home_dir, '.tmux.conf')
        self._system_run('cp %s %s' % (TMUX_DOT_TMUXCONF, home_tmux_conf))


    def _setup_vim(self, setup_config):
        vim_config = setup_config.get('vim')
        if not vim_config:
            return

        # TODO: Detect from dpkg-query -l vim-nox
        if VIM_APT_PACKAGE not in self.apt_installed_packages:
            unwanted_vim_packages = ' '.join(VIM_APT_PACKAGES_REMOVE)
            self._system_run('sudo apt-get remove -y -f %s' % unwanted_vim_packages)
            self._system_run('sudo apt-get install -y -f %s' % VIM_APT_PACKAGE)

        home_vim_dir = os.path.join(self.home_dir, '.vim')
        self._system_run('mkdir -p %s/bundle' % home_vim_dir)
        self._system_run('git clone https://github.com/gmarik/Vundle.vim.git %s/bundle/Vundle.vim' % home_vim_dir)

        home_vim_rc = os.path.join(self.home_dir, '.vimrc')
        self._system_run('cp %s %s' % (VIM_DOT_VIMRC, home_vim_rc))
        self._add_to_shell_settings(VIM_DOT_SHRC)

        self._system_run('vim +PluginInstall')


    def _setup_python(self, setup_config):
        python_config = setup_config.get('python-virtualenv')
        if not python_config:
            return

        if not self.pip_installed_packages:
            self._system_run('sudo easy_install pip')

        # TODO: Detect from pip freeze
        if PYTHON_VIRTUALENV_PIP_PACKAGE  not in self.pip_installed_packages:
            self._system_run('sudo pip install %s' % PYTHON_VIRTUALENV_PIP_PACKAGE)

        # TODO: Detect from pip freeze
        if PYTHON_VIRTUALENVWRAPPER_PIP_PACKAGE not in self.pip_installed_packages:
            self._system_run('sudo pip install %s' % PYTHON_VIRTUALENVWRAPPER_PIP_PACKAGE)

        home_python_env_dir = os.path.join(self.home_dir, '.python-env')
        self._system_run('mkdir -p %s' % home_python_env_dir)

        self._add_to_shell_settings(PYTHON_DOT_SHRC)


    def _setup_nodejs(self, setup_config):
        nodejs_versions = setup_config.get('nodejs-nvm')
        if not nodejs_versions:
            return

        # TODO: Detect from dpkg-query -l nodejs
        if NODEJS_APT_PACKAGE in self.apt_installed_packages:
            self.log.info('Node.js setup skipped, apt package installed already')
            return

        home_nvm_dir = os.path.join(self.home_dir, '.nvm')
        self._system_run('git clone git://github.com/creationix/nvm.git %s' % home_nvm_dir)

        self._add_to_shell_settings(NODEJS_DOT_SHRC)

        for version in nodejs_versions:
            self._system_run('nvm install %s' % version)


    def _get_packages_from_list(self, config, key, default_list=None):
        packages_list = config.get(key, [])

        final_packages_list = []
        if default_list:
            final_packages_list.extend(default_list)

        final_packages_list.extend(packages_list)
        return ' '.join(final_packages_list) if final_packages_list else None


    def _add_to_shell_settings(self, settings_file):
        with open(settings_file, 'r') as f:
            self.log.info('Reading settings from [%s]' % settings_file)
            data = f.read()

        with open(self.shell_settings, 'a') as f:
            self.log.info('Writing settings to [%s]' % self.shell_settings)
            f.write(data)

        self._system_run('source %s' % self.shell_settings)


    def _clean_up(self):
        self._system_run('sudo apt-get autoremove')
        self._system_run('sudo apt-get clean')
        self._system_run('sudo apt-get autoclean')


    def _system_run(self, cmdline):
        # unbuffered subprocess.Popen reference:
        # https://gist.github.com/thelinuxkid/5114777

        # Unix, Windows and old Macintosh end-of-line
        newlines = ['\n', '\r\n', '\r']

        def unbuffered(proc):
            stream_type = 'stdout'
            stream = getattr(proc, stream_type)

            # NOT CLOSING SO THAT Popen.communicate() can read from stdout again
            # with contextlib.closing(stream):
            while True:
                out = []
                last = stream.read(1)

                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break

                while last not in newlines:
                    # Don't loop forever
                    if last == '' and proc.poll() is not None:
                        break

                    out.append(last)
                    last = stream.read(1)

                out = ''.join(out)
                yield out

        self.log.debug('Executing [%s]' % cmdline)
        cmd = shlex.split(cmdline)
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                )

        for line in unbuffered(proc):
            self.log.info(line)

        out, err = proc.communicate()
        if err:
            self.log.error(err)

        if proc.returncode != 0:
            msg = 'Error running [%s]' % cmdline
            self.log.error(msg)
            raise RuntimeError(msg)


    def _logger(self):
        logging.basicConfig(level=LOG_LEVEL,
                            format=LOG_FORMAT,
                            datefmt=LOG_DATE_FORMAT)

        # Add rotating log message handler to the logger
        handler = logging.FileHandler(LOG_FILENAME,
                                               mode='w')
        handler.setLevel(LOG_LEVEL)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))

        setup_logger = logging.getLogger(LOG_NAME)
        setup_logger.addHandler(handler)

        return setup_logger


if __name__ == '__main__':
    main()
