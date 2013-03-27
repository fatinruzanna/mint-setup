Setup Python
===========

Python 2.x comes pre-installed with Linux Mint. To install Python 3.x, use the following command:

	(sudo) apt-get install python3


Setup Python Virtual Environment
---------------------------------

The virtualenv tool can be installed using easy_install or pip

1. Install easy_install, from setuptools

		(sudo) apt-get install python-setuptools


2. Install pip (optional)

		(sudo) easy_install pip


3. Install virtualenv

		(sudo) easy_install virtualenv


	**OR**

		(sudo) pip install virtualenv


4. Install virtualenvwrapper (optional)

		(sudo) easy_install virtualenvwrapper


	**OR**

		(sudo) pip install virtualenvwrapper


5. Create a directory to store Python virtual environments. An example in user directory:

		mkdir ~/python-env


Using virtualenv
-----------------

1. Create a virtual environment. Go to the Python virtual environment directory (e.g. python-env) and issue the following command:

		virtualenv <environment name>


	**Example:**

		virtualenv my-env


	This will create a directory call _my-env_ and install the necessary python modules. Parameters can be passed in to customize the virtual environment.

	To create Python environment with distribution type, _distribute_: 

		virtualenv --distribute <environment name>


	virtualenv creates a virtual environment with the default version of Python. To create Python environment with another Python version:

		virtual env --python=<path to python executable> <environment name>


	**Example:**

		virtual env --python=/usr/bin/python3.2 python32


2. Activate a virtual environment. Issue following command:

		source <path to virtual environment directory>/bin/activate


	**Example:**

		source ~/python-env/python32/bin/activate


	When a virtual environment is activated, the terminal prompt will be prefixed with the virtual environment name.

3. Deactivate current virtual environment. Issue following command:

		deactivate



To know more on virtualenv commands and parameters:

	virtualenv --help


Using virtualenvwrapper
-----------------------

virtualenvwrapper simplifies the usage of virtualenv through simpler commands. It is recommended that is installed.

1. Add into .bashrc or .bash_profile

		export WORKON_HOME="~/python-env"
		source /usr/local/bin/virtualenvwrapper.sh

	Update WORKON_HOME to the path of the directory where all the virtual environments are stored.


2. Create a virtual environment. Go to the Python virtual environment directory (e.g. python-env) and issue the following command:

		mkvirtualenv <environment name>


	**Example:**

		mkvirtualenv my-env


	Parameters of virtualenv can be passed in to customize the setup of virtual environment.


2. Activate a virtual environment. Issue following command:

		workon <environment name>


	**Example:**

		workon my-env


3. Deactivate current virtual environment. Issue following command:

		deactivate


4. Remove a virtual environment. Issue following command:

		rmvirtualenv <environment name>


	**Example:**

		rmvirtualenv my-env


5. List all virtual environments. Issue following command:

		lsvirtualenv


**References:**
* https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/

