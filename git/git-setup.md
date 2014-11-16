Setup Git
=========

Git comes pre-installed with Linux Mint.


Configure Git
-------------

The configuration below are necessary:

1. Configure your name. This will appear as the committer's name when you commit to git.

		git config --global user.name <your name>


	**Example:**

		git config --global user.name "John Doe"


2. Configure your e-mail. This will appear as the committer's e-mail when you commit to git.

		git config --global user.email <your email>
	**Example:**

		git config --global user.email "john.doe@gmail.com"


	E-mail account can be fake, but in order to be used with GitHub, the e-mail needs to be added to GitHub.


The configuration below are optional:

3. Configure for colors to be turned on when certain git commands are issued at Terminal.

		git config --global color.ui true


Setup GitHub with SSH
---------------------

1. Create RSA key using the following command:

		ssh-keygen -t rsa -C "<your e-mail here>"


	When creating SSH keys it is recommended that passphrase is set for your keys. This will ensure that if your private key falls to the wrong hands, the passphrase will be another line of defence. Your key's passphrase will need to entered everytime your key is used.

	The public and private keys will be generated in ~/.ssh directory. By default if nothing was changed during the prompt for key generation, your keys are id_rsa.pub (public key), and id_rsa (private key).

2. Copy the contents of your public key to GitHub. Issue the following command to print out your public key contents:

		cat ~/.ssh/id_rsa.pub

	At GitHub go to GitHub Settings > SSH Keys. Add your public key contents and give an appropriate description.

3. Add both  your public and private keys to ssh-agent. This will allow ssh-agent to manage your keys.

		ssh-add


4. View list of your ssh keys registered to ssh-agent

		ssh-add -l


5. Setup github.com as a known host.

		ssh -T git@github.com


	**NOTE:** Enter _yes_ when prompted. DO NOT JUST PRESS ENTER!!!

	This will add github.com to your list of known hosts, saved in ~/.ssh/known_hosts file.


**References:**
* https://help.github.com/articles/generating-ssh-keys
* https://help.github.com/articles/set-up-git


Update Terminal Prompt with Git branch
--------------------------------------

1. Clone git repository

		git clone git://git.kernel.org/pub/scm/git/git.git ~/.git


2. Copy git-completion.bash to */bin/

		cp ~/.git/contrib/completion/git-completion.bash ~/bin/git/git-completion.sh
		mkdir ~/bin/git
		chmod u+x ~/bin/git/git-completion.sh


3. Remove the git repository

		rm -rf ~/.git


4. Add to your .bashrc file with the contents in _bashrc_ file, and source your .bashrc file

		source ~/.bashrc


**References:**
* http://wiki.collectionspace.org/display/~aronr/Displaying+the+current+git+branch+in+your+command+prompt+(Unix-like+systems)
* https://blogs.oracle.com/linuxnstuff/entry/recommended_git-completionbash
* http://www.edmondscommerce.co.uk/linux/tip-have-git-branch-displayed-in-bash-prompt/

