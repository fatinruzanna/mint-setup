install = {
    'apt':  {
        'uninstall': [
        ],
        'install': [
            'curl',
            'openssl',
            'git',
            'gitk',
            'meld',
            'python3-dev',
            'chromium',
        ],
    },
    'ruby': {
        'global': {
            'uninstall': {
            },
            'install': {
            },
        },
    },
    'python': {
        'global': {
            'uninstall': {
            },
            'install': {
                'ipython': '*'
            },
        },
        'user': {
            'uninstall': {
            },
            'install': {
                'awscli': '*'
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
        'enable': True,
        'config': {
            'distribution': 'ubuntu',  # accepted values: debian, ubuntu
        }
    },
    'git': {
        'enable': True,
        'config': {
            "name": "Fatin Ruzanna",
            "email": "fatin.ruzanna+gh@gmail.com",
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