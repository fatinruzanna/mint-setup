Setup Vim
=========

Uninstall other variations of Vim:

		(sudo) apt-get remove vim vim-runtime gvim  vim-tiny vim-common vim-gui-common


To install Vim-Nox, use the following command:

		(sudo) apt-get install vim-nox


Configure Vim
--------------

1. Setup Vundle

		mkdir -p ~/.vim/bundle
		git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim


2. Create .vimrc file

		touch ~/.vimrc


3. Add to your .vimrc file with the contents in _vimrc_ file.


4. Install Vundle plugins

		vim +PluginInstall


5. Set Vim as your default text editor. Add to your .bashrc or .zshrc file with the contents in _bashrc_ file, and source your .bashrc or .zshrc file:

        source ~/.bashrc


**References:**
* https://www.codementor.io/linux-tutorial/configure-linux-toolset-zsh-tmux-vim
