mint-setup
==========

Set up Debian/Ubuntu based Linux distribution as your Workstation or virtual machine

Basic setup
-----------

1. Ensure user is in sudoers list. If not add user as sudoer.

		su
		adduser <insert your username here> sudo

2. Log out and re-log in to refresh sudoers list

3. Install basic dependencies

		sh bootstrap


Install virtual machine dependencies
------------------------------------

a. (Optional) For VMWare, install open-vm-tools

	(sudo) apt-get install open-vm-tools open-vm-tools-desktop open-vm-tools-dev

b. (Optional) For Virtualbox, install Virtualbox Guest Additions

* From the virtual machine menu, select the “Devices -> CD/DVD Devices -> Choose a virtual CD/DVD disk file” option. Select the VBoxGuestAdditions.iso file.

* The VBoxGuestAdditions.iso file is usually located in the /usr/share/virtualbox/ directory on Linux, in the C:\Program Files\Oracle\VirtualBox directory on Windows and the Contents/MacOS directory of the VirtualBox package on Mac OS X.

* Mount the CD-ROM and install the VirtualBox Guest Additions:

		(sudo) sh ./VBoxLinuxAdditions.run


Install the rest of the dependencies
------------------------------------

1. Reboot

2. TBC
