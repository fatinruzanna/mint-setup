Setup Zsh
=========

To install Zsh, use the following command:

		(sudo) apt-get install zsh


Switch default shell to Zsh:

		(sudo) chsh -s $(which zsh)


Setup oh-my-zsh
----------------

1. Clone oh-myzsh:

		git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh


2. Create .zshrc file

		touch ~/.zshrc


3. Add to your .zshrc file with the contents in _zshrc_ file, and source your .zshrc file

		source ~/.zshrc


4. Logout from Linux and re-login.


**References:**
* https://www.codementor.io/linux-tutorial/configure-linux-toolset-zsh-tmux-vim
