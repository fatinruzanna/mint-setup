Setup Node.js
=============

Setup Node.js Version Manager (NVM)
-----------------------------------

**Pre-requisite:** Git


Since Node.js is still in active development (it has yet to reach ver. 1.0!), it useful to have a tool that allows you to install multiple versions of Node.js on your machine. When a new version is released, you may want to test your application with the new version before using it in production.

Please refer to the last section if you do not wish to use NVM.

1. Clone the git repository to your local machine:

		git clone git://github.com/creationix/nvm.git ~/.nvm


2. Add to your .bashrc or .zshrc file with the contents in _bashrc_ file, and source your .bashrc or .zshrc file:

		source ~/.bashrc

	Update **NVM_HOME** to the path of the directory where nvm repository was clone at, if you did not follow these instructions to the dot.


Using NVM
---------

1. Install a Node.js version. Issue the following command:

		nvm install v<node.js version number>

	**Example:**

		nvm install v0.10.1


2. List all installed versions of Node.js. Issue the following command:

		nvm ls


3. Use a specific installed version of Node.js. Issue the following command:

		nvm use v<node.js version number>


	**OR**

		nvm run v<node.js version number>


	**Example:**

		nvm use v0.10.1


	**OR**

		nvm run v0.10.1


4. Deactivate selected version. Issue the following command:

		nvm deactivate


5. Set default version of Node.js, which will be used each time you open a new Terminal. This saves your time from running _nvm run_ or _nvm use_. Issue the following command:

		nvm alias default <major version>.<minor version>


	**Example:**

		nvm alias default 0.10


	**NOTE:** Only major and minor versions are required. In the example given, NVM will use the latest 0.10.x version


**References:**
* https://github.com/brianloveswords/nvm


Setup Node.js without NVM
-------------------------

1. Issue following command to install node.js:

		(sudo) apt-get install nodejs

