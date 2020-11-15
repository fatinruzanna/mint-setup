install = {
    'apt':  {
        'uninstall': [
        ],
        'install': [
            'caja-open-terminal',
            'chromium',
            'curl',
            'openssl',
        ],
    },
    'ruby': {
        'uninstall': [
        ],
        'install': [
        ],
    },
    'python': {
        'uninstall': [
        ],

        # For package to install, specify package and desired version
        #   Latest: 
        #       'ipython': '*'
        #   Specific version:
        #       'ipython': '==7.19.0'
        #   Minimum version:
        #       'ipython': '>=7.19.0'

        'install': {
            'global': {
                'ipython': '*',
            },

            # TODO: Installing within user context not available when in virtualenv
            'user': {
                'awscli': '*',
            },
        },
        
    },
}

download = {
    # Each item in the list consists of
    #   source: str
    #   filename: str

    'deb': [
        {
            'filename': 'vs-code.deb',
            'source': 'https://go.microsoft.com/fwlink/?LinkID=760868',
        },
    ],
    'misc': [
        {
            'filename': 'pycharm-professional-2020.2.3.tar.gz',
            'source': 'https://download.jetbrains.com/python/pycharm-professional-2020.2.3.tar.gz',
        },
    ]
}

setup = {
    'docker': {
        'enable': False,
        'config': {
            'distribution': 'ubuntu',  # accepted values: debian, ubuntu
            'release': 'focal',  # specify Ubuntu release when using other distribution based from Ubuntu like Linux Mint
            'compose_version': '1.27.4',
        }
    },
    'git': {
        'enable': True,
        'config': {
            'name': 'Fatin Ruzanna',
            'email': 'fatin.ruzanna+gh@gmail.com',
            'set_up_bash': True,
        },
    },
    'sublime_text': {
        'enable': True,
        'config': {
        }
    },
    'tmuxinator': {
        'enable': False,
        'config': {
        }
    },
    'vim_nox': {
        'enable': False,
        'config': {
        }
    },
    'zsh': {
        'enable': True,
        'config': {
        }
    },
}
