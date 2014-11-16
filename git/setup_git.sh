#!/bin/bash
# Argument = -i install -s setup -d directory -n name -e email

usage()
{
cat << EOF
usage: $0 options

This script installs and setup git configurations.

OPTIONS:
   -h      Show this message
   -i      Install git
   -s      Setup git configurations
   -d      Master directory name at ~/ to place git repositories
   -n      Git configuration  - User name
   -e      Git configuration - E-mail address
EOF
}

INSTALL_GIT=
SETUP_GIT=
MASTER_DIRECTORY=
GIT_USERNAME=
GIT_EMAIL=
CWD=$(pwd)

while getopts “his:d:n:e” OPTION
do
    case $OPTION in
        h)
            usage
            exit 1
            ;;
        i)
            INSTALL_GIT=$OPTARG
            ;;
        s)
            SETUP_GIT=$OPTARG
            ;;
        d)
            MASTER_DIRECTORY="~/" + $OPTARG
            ;;
        n)
            GIT_USERNAME=1
            ;;
        e)
            GIT_EMAIL=1
            ;;
        ?)
            usage
            exit
            ;;
    esac
done

if [[ !$INSTALL_GIT ]] && [[ !$SETUP_GIT ]]
then
     usage
     exit 1
fi

if [[ $INSTALL_GIT ]]
then
    sudo apt-get install -y git
fi

if [[ $SETUP_GIT ]]
then
    git config --global user.name $GIT_EMAIL
    git config --global user.email $GIT_EMAIL
    git config --global color.ui true

    mkdir $MASTER_DIRECTORY
    cd $MASTER_DIRECTORY
    git clone git://git.kernel.org/pub/scm/git/git.git
    cp $MASTER_DIRECTORY/git/contrib/completion/git-completion.bash git-completion.sh
    chmod u+x git-completion.sh
    mkdir ~/bin
    mv git-completion.sh ~/bin
    cd $CWD
    cat ./bashrc >> ~/.bashrc
    source ~/.bashrc
fi
