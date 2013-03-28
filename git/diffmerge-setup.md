Setup DiffMerge for Git
========================

**Pre-requisite:**
* Git


----


1. Install DiffMerge tool (DiffMerge for Ubuntu) from http://www.sourcegear.com/diffmerge/.

2. Downloaded file is a Debian package (.deb file). Double-click the file to run installation.

3. Run the following commands to setup mergetool for git:

		git config --global merge.tool diffmerge
		git config --global mergetool.diffmerge.cmd "diffmerge --merge --result=\$MERGED \$LOCAL \$BASE \$REMOTE"
		git config --global mergetool.diffmerge.trustExitCode true
		git config --global mergetool.keepBackup false


	To run mergetool, issue the following command:

		git mergetool


4. Run the following commands to setup difftool for git:

		git config --global diff.tool diffmerge
		git config --global difftool.diffmerge.cmd "diffmerge \$LOCAL \$REMOTE"


	To run mergetool, issue the following command:

		git difftool


	**OR**

		git difftool <base branch or commit hash> <change branch or commit hash>


**References:**
* http://adventuresincoding.com/2010/04/how-to-setup-git-to-use-diffmerge

