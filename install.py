import os
import pwd
import contextlib
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
        self.user = pwd.getpwuid(os.getuid())[0]
        self.setup_summary = []


    def run(self):

        self.log.debug('*** INSTALLATION AND SETUP STARTING ... ***')

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
        self._setup_tmux(setup_config)
        self._setup_vim(setup_config)
        self._setup_python(setup_config)
        self._setup_nodejs(setup_config)

        # clean up
        self._clean_up()

        self._print_setup_summary()

        self.log.debug('*** ... THE END ***')


    def _run_apt(self):
        apt_config = self.config.get('apt')
        if not apt_config:
            return

        uninstall_packages = apt_config.get('remove', [])
        if uninstall_packages:
            self.log.debug('*** Uninstalling apt packages ***')
            for package in uninstall_packages:
                self._system_run(['sudo', 'apt-get', 'remove', '-y', package])

        install_packages = []
        install_packages.extend(DEFAULT_APT_INSTALL)
        install_packages.extend(apt_config.get('install', []))
        if install_packages:
            self.log.debug('*** Updating apt packages ***')
            self._system_run(['sudo', 'apt-get', 'update'])

            self.log.debug('*** Installing apt packages ***')
            for package in install_packages:
                self._system_run(['sudo', 'apt-get', 'install', '-y', '-f', package])

        self.apt_installed_packages = install_packages


    def _run_gem(self):
        gem_config = self.config.get('gem')
        if not gem_config:
            return

        uninstall_packages = gem_config.get('uninstall', [])
        install_packages = gem_config.get('install', [])

        if uninstall_packages or install_packages:
            self.log.debug('*** Installing ruby to get rubygems ***')
            self._system_run(['sudo', 'apt-get', 'install', '-y', '-f', 'ruby'])

        if uninstall_packages:
            self.log.debug('*** Uninstalling gem packages ***')
            for package in uninstall_packages:
                self._system_run(['sudo', 'gem', 'uninstall', package])

        if install_packages:
            self.log.debug('*** Installing gem packages ***')
            for package in install_packages:
                self._system_run(['sudo', 'gem', 'install', package])

        self.gem_installed_packages = install_packages


    def _run_pip(self):
        pip_config = self.config.get('pip')
        if not pip_config:
            return

        uninstall_packages = pip_config.get('uninstall', [])
        install_packages = pip_config.get('install', [])

        if uninstall_packages or install_packages:
            self.log.debug('*** Installing pip ***')
            self._system_run(['sudo', 'easy_install', 'pip'])

        if uninstall_packages:
            self.log.debug('*** Uninstalling pip packages ***')
            for package in uninstall_packages:
                self._system_run(['sudo', 'pip', 'uninstall', package])

        if install_packages:
            self.log.debug('*** Installing pip packages ***')
            for package in install_packages:
                self._system_run(['sudo', 'pip', 'install', package])

        self.pip_installed_packages = install_packages


    def _run_wget(self):
        wget_config = self.config.get('wget')
        if not wget_config:
            return

        home_download_directory = os.path.join(self.home_dir, 'Downloads')
        download_packages = wget_config.get('download')
        if download_packages:
            self.log.debug('*** Installing wget ***')
            self._system_run(['sudo', 'apt-get', 'install', '-y', '-f', 'wget'])

            self.log.debug('*** Downloading files with wget ***')
            for package in download_packages:
                self._system_run(['wget', '-P', home_download_directory, package])


    def _setup_shell_settings(self, setup_config):
        setup_zsh = setup_config.get('zsh')

        if not setup_zsh:
            settings_file = '.bashrc'
        else:
            settings_file = '.zshrc'

        home_settings_file = os.path.join(self.home_dir, settings_file)
        self.shell_settings = home_settings_file

        self.log.debug('*** Creating shell config file %s ***' % home_settings_file)
        self._system_run(['touch', home_settings_file])

        self._add_to_setup_summary('Shell config file: %s' % home_settings_file)

        self._setup_zsh(setup_config)


    def _setup_git(self, setup_config):
        git_config = setup_config.get('git')
        if not git_config:
            return

        name = git_config.get('name')
        email = git_config.get('email')

        # TODO: Detect from dpkg-query -l git
        self.log.debug('*** Setting up git configurations ***')
        if GIT_APT_PACKAGE not in self.apt_installed_packages:
            self._system_run(['sudo', 'apt-get', 'install', '-y', '-f', GIT_APT_PACKAGE])

        self.log.debug('*** Setting up ~/.gitconfig ***')
        home_dot_gitconfig = os.path.join(self.home_dir, '.gitconfig')
        self._system_run(['cp', GIT_DOT_GITCONFIG, home_dot_gitconfig])

        if name:
            self._system_run(['git', 'config', '--global', 'user.name', '"%s"' % name])

        if email:
            self._system_run(['git', 'config', '--global', 'user.email', '"%s"' % email])

        # TODO: Check version!!! Below is for >= 1.7.9:
        # self._system_run(['git', 'config', '--global pull.rebase', 'true'])
        # TODO: Check version!!! Below is for < 1.7.9:
        # self._system_run(['git', 'config', '--global branch.autosetuprebase', 'always'])

        self._add_to_setup_summary('Git config file: %s' % home_dot_gitconfig)

        if 'bashrc' in self.shell_settings:
            self.log.debug('*** Setting up ~/.bashrc with git completion and terminal prompt ***')

            local_git_repo = os.path.join(self.home_dir, '.git')
            git_bin_dir = os.path.join(self.home_dir, 'bin/git')
            if not os.path.exists(local_git_repo):
                self._system_run(['git', 'clone', 'git://git.kernel.org/pub/scm/git/git.git', local_git_repo])

            self._system_run(['mkdir', '-p', git_bin_dir])
            self._system_run(['cp', '%s/contrib/completion/git-completion.bash' % local_git_repo, '%s/git-completion.sh' % git_bin_dir])
            self._system_run(['chmod', 'u+x', '%s/git-completion.sh' % git_bin_dir])
            self._system_run(['rm', '-rf', local_git_repo])
            self._add_to_shell_settings(GIT_DOT_SHRC)

            self._add_to_setup_summary('Git completion and terminal prompt configured: %s' % self.shell_settings)


    def _setup_zsh(self, setup_config):
        zsh_config = setup_config.get('zsh')
        if not zsh_config:
            return

        # TODO: Detect from dpkg-query -l zsh
        self.log.debug('*** Setting up Zsh ***')
        if ZSH_APT_PACKAGE not in self.apt_installed_packages:
            self._system_run(['sudo', 'apt-get', 'install', '-y', '-f', ZSH_APT_PACKAGE])

        self.log.debug('*** Switch shell to Zsh ***')
        self._system_run(['sudo', 'chsh', '-s', '/bin/bash', self.user])

        self.log.debug('*** Setting up oh-my-zsh ***')
        home_ohmyzsh_repo = os.path.join(self.home_dir, '.oh-my-zsh')
        if not os.path.exists(home_ohmyzsh_repo):
            self._system_run(['git', 'clone', 'git://github.com/robbyrussell/oh-my-zsh.git', home_ohmyzsh_repo])

        self.log.debug('*** Setting up ~/.zshrc ***')
        self._add_to_shell_settings(ZSH_DOT_ZSHRC, source_file=False)

        self._add_to_setup_summary('oh-my-zsh repository: %s' % home_ohmyzsh_repo)


    def _setup_tmux(self, setup_config):
        tmux_config = setup_config.get('tmux')
        if not tmux_config:
            return

        # TODO: Detect from dpkg-query -l tmux
        self.log.debug('*** Setting up Tmux ***')
        if TMUX_APT_PACKAGE not in self.apt_installed_packages:
            self._system_run(['sudo', 'apt-get', 'install', '-y', '-f', TMUX_APT_PACKAGE])

        self.log.debug('*** Setting up ~/.tmux.conf ***')
        home_tmux_conf = os.path.join(self.home_dir, '.tmux.conf')
        self._system_run(['cp', TMUX_DOT_TMUXCONF, home_tmux_conf])

        self._add_to_setup_summary('Tmux config file: %s' % home_tmux_conf)


    def _setup_vim(self, setup_config):
        vim_config = setup_config.get('vim')
        if not vim_config:
            return

        # TODO: Detect from dpkg-query -l vim-nox
        self.log.debug('*** Setting up Vim ***')
        if VIM_APT_PACKAGE not in self.apt_installed_packages:
            for unwanted_vim_package in VIM_APT_PACKAGES_REMOVE:
                self._system_run(['sudo', 'apt-get', 'remove', '-y', '-f', unwanted_vim_package])
            self._system_run(['sudo', 'apt-get', 'install', '-y', '-f', VIM_APT_PACKAGE])

        self.log.debug('*** Setting up Vundle***')
        home_vim_dir = os.path.join(self.home_dir, '.vim')
        self._system_run(['mkdir', '-p', '%s/bundle' % home_vim_dir])
        if not os.path.exists(home_vim_dir):
            self._system_run(['git', 'clone', 'https://github.com/gmarik/Vundle.vim.git', '%s/bundle/Vundle.vim' % home_vim_dir])

        self.log.debug('*** Setting up ~/.vimrc ***')
        home_vim_rc = os.path.join(self.home_dir, '.vimrc')
        self._system_run(['cp', VIM_DOT_VIMRC, home_vim_rc])
        self._add_to_shell_settings(VIM_DOT_SHRC)

        #self.log.debug('*** Installing Vundle plugins ***')
        #self._system_run(['vim', '+PluginInstall'])

        self._add_to_setup_summary('*** DON\'T FORGET TO RUN... vim +PluginInstall')
        self._add_to_setup_summary('Vim config file: %s' % home_vim_rc)
        self._add_to_setup_summary('Vim Vundle repository: %s/bundle/Vundle.vim' % home_vim_dir)


    def _setup_python(self, setup_config):
        python_config = setup_config.get('python-virtualenv')
        if not python_config:
            return

        self.log.debug('*** Setting up Python virtual environments ***')
        if not self.pip_installed_packages:
            self._system_run(['sudo', 'apt-get', 'install', '-y', '-f', 'python-setuptools'])
            self._system_run(['sudo', 'easy_install', 'pip'])

        # TODO: Detect from pip freeze
        if PYTHON_VIRTUALENV_PIP_PACKAGE  not in self.pip_installed_packages:
            self._system_run(['sudo', 'pip', 'install', PYTHON_VIRTUALENV_PIP_PACKAGE])

        # TODO: Detect from pip freeze
        if PYTHON_VIRTUALENVWRAPPER_PIP_PACKAGE not in self.pip_installed_packages:
            self._system_run(['sudo', 'pip', 'install', PYTHON_VIRTUALENVWRAPPER_PIP_PACKAGE])

        self.log.debug('*** Creating ~/.python-env directory ***')
        home_python_env_dir = os.path.join(self.home_dir, '.python-env')
        self._system_run(['mkdir', '-p', home_python_env_dir])

        self.log.debug('*** Setting up shell config with virtualenvwrapper startup ***')
        self._add_to_shell_settings(PYTHON_DOT_SHRC)

        self._add_to_setup_summary('Python virtual environments directory: %s' % home_python_env_dir)
        self._add_to_setup_summary('virtualenvwrapper shell setup configured: %s' % self.shell_settings)


    def _setup_nodejs(self, setup_config):
        nodejs_versions = setup_config.get('nodejs-nvm')
        if not nodejs_versions:
            return

        # TODO: Detect from dpkg-query -l nodejs
        self.log.debug('*** Setting up NVM ***')
        if NODEJS_APT_PACKAGE in self.apt_installed_packages:
            self.log.info('Node.js setup skipped, apt package installed already')
            return

        home_nvm_dir = os.path.join(self.home_dir, '.nvm')
        if not os.path.exists(home_nvm_dir):
            self._system_run(['git', 'clone', 'git://github.com/creationix/nvm.git', home_nvm_dir])

        self.log.debug('*** Setting up shell config with nvm startup ***')
        self._add_to_shell_settings(NODEJS_DOT_SHRC)

        #self.log.debug('*** Installing Node.js versions ***')
        #for version in nodejs_versions:
            #self._system_run(['nvm', 'install', version])

        self._add_to_setup_summary('*** DON\'T FORGET TO RUN... nvm install %s' % nodejs_versions[-1])
        self._add_to_setup_summary('NVM shell setup configured: %s' % self.shell_settings)
        self._add_to_setup_summary('NVM repository: %s' % home_nvm_dir)


    def _get_packages_from_list(self, config, key, default_list=None):
        packages_list = config.get(key, [])

        final_packages_list = []
        if default_list:
            final_packages_list.extend(default_list)

        final_packages_list.extend(packages_list)
        return ' '.join(final_packages_list) if final_packages_list else None


    def _add_to_shell_settings(self, settings_file, source_file=True):
        with open(settings_file, 'r') as f:
            self.log.info('*** Reading settings from [%s] ***' % settings_file)
            data = f.read()

        with open(self.shell_settings, 'a') as f:
            self.log.info('*** Writing settings to [%s] ***' % self.shell_settings)
            f.write(data)

        if source_file:
            self._system_run(['bash', '-c', 'source %s' % self.shell_settings])


    def _add_to_setup_summary(self, log):
        if isinstance(log, basestring):
            self.setup_summary.append(log)


    def _clean_up(self):
        self._system_run(['sudo', 'apt-get', 'autoremove'])
        self._system_run(['sudo', 'apt-get', 'clean'])
        self._system_run(['sudo', 'apt-get', 'autoclean'])


    def _print_setup_summary(self):
        if not self.setup_summary:
            return

        self.log.info('')
        self.log.info('*****************************************************')
        self.log.info('*                      SUMMARY                      *')
        self.log.info('*****************************************************')
        self.log.info('')

        for line in self.setup_summary:
            self.log.info(line)

        self.log.info('')
        self.log.info('*****************************************************')
        self.log.info('')


    def _system_run(self, cmd):
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

        cmdline = ' '.join(cmd)
        self.log.debug('*** Executing [%s] ***' % cmdline)
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
            msg = ' *** Error running [%s] ***' % cmdline
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
