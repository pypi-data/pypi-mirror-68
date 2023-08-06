from setuptools import setup
from textwrap import dedent

# create README file by combining sshdeploy/manual.rst with the following 
# installation instructions
install = dedent("""\
    Installation
    ============

    If you plan to use SSH Deploy without modifying it, the preferred way to 
    install it for multiple users is::

       pip install --update sshdeploy

    Doing so generally requires root permissions. Alternately, you can install it 
    just for yourself using::

       pip install --user --update sshdeploy

    This installs sshdeploy into ~/.local and so does not require root permissions.

    If you would like to change the program, you should first clone it's source 
    repository and then install it::

       git clone https://github.com/KenKundert/sshdeploy.git
       cd sshdeploy
       python setup.py install --user
""")
with open('sshdeploy/manual.rst') as f:
    manual = f.read()
with open('README.rst', 'w') as f:
    readme ='\n\n'.join([manual, install])
    f.write(readme)

setup(
    name = 'sshdeploy',
    version = '1.2.0',
    description = "Generates and distributes SSH keys.",
    long_description = readme,
    author = "Ken Kundert",
    author_email = 'sshdeploy@nurdletech.com',
    url = 'http://nurdletech.com/linux-utilities/sshdeploy',
    download_url = 'https://github.com/kenkundert/sshdeploy/tarball/master',
    entry_points = {
        'console_scripts': [
            'sshdeploy=sshdeploy.main:main',
        ],
    },
    zip_safe = False,
    packages = ['sshdeploy'],
    package_data = {'sshdeploy': ['manual.rst']},
    license = 'GPLv3+',
    install_requires = [
        'arrow',
        'docopt',
        'inform',
        'pexpect',
        'shlib',
        'avendesora',
    ],
    keywords = [
        'ssh',
        'keys',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
)
# vim: set sw=4 sts=4 et:
