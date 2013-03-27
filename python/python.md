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

	OR

	(sudo) pip install virtualenv

4. Install virtualenvwrapper (optional)

	(sudo) easy_install virtualenvwrapper

	OR

	(sudo) pip install virtualenvwrapper

5. Add into .bashrc or .bash_profile (optional)
   NOTE: Only required if virtualenvwrapper is installed

	export WORKON_HOME="~/python-env"
	source /usr/local/bin/virtualenvwrapper.sh
