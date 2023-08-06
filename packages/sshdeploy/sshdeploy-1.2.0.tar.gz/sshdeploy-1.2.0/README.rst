---------------------------------------------
SSH Deploy - Generate and Distribute SSH Keys
---------------------------------------------


SYNOPSIS
========

sshdeploy [options] generate
sshdeploy [options] test
sshdeploy [options] hosts
sshdeploy [options] distribute
sshdeploy [options] clean
sshdeploy manual


OPTIONS
=======

-c <file>, --config-file <file>   file that contains list of keys to generate nd 
                                  the hosts that should receive the keys 
                                  (sshdeploy.conf is default).
-d <name>, --keydir <name>        name of directory for holding new keys
                                  (keys-YYYY-MM-DD is default).
-u <hosts>, --update <hosts>      hosts to update
-s <hosts>, --skip <hosts>        hosts to skip
-k <keys>, --keys <keys>          keys to update (only use with --trial-run)
-t, --trial-run                   trial run (do not overwrite working ssh files)
-n, --narrate                     narrate the process
-v, --verbose                     narrate the process more verbosely
-h, --help                        print usage summary

You specify multiple hosts or keys using a comma-separated list.

With the --trial-run (or -t) option sshdeploy still generates the keys and 
copies them  to the remote hosts, but when doing so it will add '.provisional' 
as a suffix to the files to that they do not overwrite existing working files.   


DESCRIPTION
===========

SSH Deploy reads a configuration file that contains information about the SSH 
keys you use.  Using this information it regenerates and distributes your keys.  
When generating your keys a passcode is needed.  SSH Deploy uses the Avendesora 
collaborative password generator to securely generate the passcodes.  This 
avoids the need for you to interactively enter the passcodes.

sshdeploy generate
******************

The generate command regenerates the SSH key pairs.

sshdeploy distribute
********************

The distribute command copies the SSH key pair to to the clients and the 
authorized_keys files to the servers.  It can only be run after the generate key 
has been run.  Before it runs it will clean out any .provisional files from 
previous trial runs.

sshdeploy test
**************

The test command checks the connection with each of the hosts (the clients and 
servers).  It should be run before *distribute* to assure that each of the 
hosts is accessible.

sshdeploy hosts
***************

The hosts command simply lists out the hosts. Hosts include the servers that 
are to receive the authorized_keys file and the clients that are to receive the 
SSH key pairs.

sshdeploy clean
***************

The clean command removes the .provisional files from each of the hosts.  The 
.provisional files are created during a trial run of the *distribute* command.

sshdeploy manual
****************

The manual command displays a detailed description of the program and how to use 
it.

.. warning::

    This program is not recommended for general use. It has a fundamental flaw 
    during the update process that overwrites critical files, resulting in the 
    update process breaking down midstream. If this occurs you may be locked out 
    of your servers.  It is possible to work around the problem by skipping the 
    update of your local machine and then manually performing that update later.


CONFIGURATION
=============

The configuration file is a python file.  The name of the file is arbitrary (the 
default is sshdeploy.conf).  Here is a typical configuration file::

    Keys = {
        'earth': {
            'purpose': 'This key allows access from earth (primary laptop)',
            'keygen_options': "-t ed25519",
            'servers': {
                'earth': {},
                'mercury': {
                    'description': 'Access is funneled through Jupiter',
                    'restrictions': ['from=jupiter']
                },
                'jupiter': {},
            },
            'clients': {
                'earth': {},
            },
        },
        'phone': {
            'purpose': "This key allows access from the phone",
            'servers': {
                'jupiter': {
                    'description': 'Only allows access to mail ports',
                    'restrictions': [
                        'no-agent-forwarding',
                        'no-pty',
                        'no-X11-forwarding',
                        'permitopen="pubmail:587"',
                        'permitopen="pubmail:993"',
                    ],
                },
            },
        },
        'backups': {
            'purpose': "This key allows sftp access to jupiter for backups.",
            'servers': {
                'jupiter': {
                    'description': 'This key is not protected with a passphrase!',
                    'restrictions': [
                        'from="192.168.1.0/24"',
                        'no-agent-forwarding',
                        'no-port-forwarding',
                        'no-pty',
                        'no-X11-forwarding',
                        'command=".ssh/only-sftp.sh"',
                    ],
                },
            },
            'clients': {
                'earth': {},
                'mercury': {},
            },
        },
    }

When sshdeploy reads this file, it uses the value of several local variables 
('keygen_options', 'avendesora_account', 'remote_include_filename', and 'keys') to 
determine its behavior.


Keygen Options
**************

A string that is passed to ssh-keygen to influence the generation of key.  If 
not specified, the following will be used: '-t rsa -b 4096'.  This value is used 
as the default for all keys and its value may be overridden in individual keys.


Avendesora Account
******************

When the private keys are generated a passcode is needed to secure the private 
key.  SSH Deploy uses the Avendesora password manager to provide the needed 
passcodes.  The value of this variable is a string that is used as the default 
Avendesora account name for for all keys and its value may be overridden in 
individual keys.


Remote Include Filename
***********************

Before SSH Deploy generates an authorized_keys file for a server, it will look 
for a file in the server's ~/.ssh directory that contains public keys for keys 
not managed by SSH Deploy that should be included in the authorized_keys file.  
The value of this variable is the name of that file.


Keys
****

Keys is a dictionary where there is one entry per SSH key to be generated.  The 
tag for the entry is the name of the SSH key and the value is a dictionary that 
contains information that controls how the key is generated and distributed.  
These dictionaries may contain the keys 'purpose', 'keygen_options', 
'avendesora_account', 'servers', and 'clients'.


Purpose
-------

The purpose if given is simply a textual description of the purpose of
the key.  It will be added as a comment above the public key when it is
added to the authorized key file.


Keygen Options
--------------

A string that is passed to ssh-keygen to influence the generation of
key.  If not specified, the following will be used: '-t rsa -b 4096'.


Avendesora Account
------------------

When the private keys are generated a passcode is needed to secure the private 
key.  SSH Deploy uses the Avendesora password manager to provide the needed 
passcodes.  This value overrides the default value for this particular key.  If 
the value is specified as None, then the private key will not be protected by 
a passcode.


Servers
-------

The servers key contains a dictionary where its keys would be the SSH
names of servers whose authorized_keys file that should receive the
public key.  The value of the servers key is also a dictionary that may
be empty or may contain the following keys: 'description', 'restrictions', 
'remote_include_filename', and 'bypass'.


Description
'''''''''''

The description is simply a second level of textual description for the
public key (generally explains the restrictions).


Restrictions
''''''''''''

The value of restrictions is a list of SSH key restrictions.  These
restrictions are comma joined and placed before the public key in the
authorized key file.


Remote Include Filename
'''''''''''''''''''''''

Before SSH Deploy generates an authorized_keys file for a server, it will look 
for a file in the server's ~/.ssh directory that contains public keys for keys 
not managed by SSH Deploy that should be included in the authorized_keys file.  
The value of this variable is the name of that file.

In a configuration file the same server may be referenced many times, once per 
key.  The remote include file is only read the first time a server is 
encountered (they are processed in alphabetic order).  It is recommended that 
if this value is given, it be given consistently in each instance of a server, 
otherwise warnings will be issued and each value except the first will be 
ignored.

If the value is None, an include is not performed.


Bypass
''''''

Some servers, particularly commercial cloud servers, do not allow you to upload 
an authorized_keys file using sftp.  Instead they generally provide a way 
through their web portal.  In these cases you should specify bypass to be true.  
Doing so will prevent sshdeploy from attempting to upload the file and will 
cause it to emit a warning that acts as a reminder that you must upload your 
file manually.


Clients
-------

The clients key contains a dictionary where its keys would be the SSH
names of client hosts that should receive the private and public key.
The value of the clients key is also a dictionary that should be empty
(at this point any contents will be ignored).


KEY STRATEGIES
==============

Several key strategies can be implemented efficiently with SSH Deploy.


One Key Per Server
******************

With this strategy SSH keys are never shared between servers, meaning that one 
server could not use its key to access another.  Normally this cross access 
would not be possible anyway, but if there were a bug in SSH it could 
conceivably leak the private key to an untrusted server.  Since in this strategy 
the key for each server is unique, a leak would not compromise the other 
servers.


One Key Per Client
******************

With this strategy the server can distinguish the client that is requesting 
a connection.  Thus a particular client can be blocked or restrictions placed on 
its access.


Other Strategies
****************

Using single key for each server/client pair can give the best security and 
flexibility, but may be tedious to configure and maintain.  Alternatively, you 
might adapt your strategy to provide the security and flexibility appropriate to 
you various servers and clients.


DISTRIBUTING YOUR KEYS
======================

Distributing your keys is inherently a dangerous endeavor because if you make 
a mistake you will likely lose the ability to log into one of your hosts, which 
would prevent you from fixing the mistake.  To reduce the risk of being locked 
out of a remote host, sshdeploy several features that reduce the risk.  One is 
the test command, which allows you to verify that all of your hosts are 
available before you update your keys, and that they are still available after 
you update them.  Another feature is the --trial-run option.  When specified, 
sshdeploy will add the .provisional suffix to any file it copies to a remote 
host.  Thus, the basic strategy is to run distribute command with the 
--trial-run option while carefully examining the provisional files to make sure 
everything working as expected.  Running sshdeploy with many keys and hosts can 
be time consuming, so several command line options are provide that allow you 
to limit your activities to particular keys (--keys) and servers (--update, 
--skip).  In addition, sshdeploy also provides the --narrate and --verbose 
options to make sshdeploy's activities more obvious to you.

Once you are confident that things are configured properly, it is recommended 
that you follow the following process to generate and distribute your ssh keys.

1. Generate your new keys with::

      sshdeploy generate

2. Make sure all of your hosts (servers and clients) are up and accessible.  You 
   can do that with::

      sshdeploy test

   However, it is even better for you to simply open and keep active a ssh or 
   sftp process to each of the remote hosts.  Leave them open until all of your 
   hosts are known to work.  That way if there is a problem that corrupts the 
   authorized_keys file, you still have access and can correct any problems.

3. Do a full trial run of distribute::

      sshdeploy -t distribute

   Confirm that provisional versions of all of your ssh keys and authorized_keys 
   files are being properly created and distributed to all of your hosts.  You 
   can first look in the keys directory to make sure the right authorized_keys 
   files are generate.  Then you should check the .provisional files on the 
   remote hosts.

4. Run distribute for real::

      sshdeploy distribute

   Do not add --trial-run, --update, --skip, or --keys to the list of command 
   line options.

5. Immediately after the update, start a new ssh-agent in a new shell and add 
   your new keys.  If you have ControlMaster in your SSH config file, you should 
   remove it for the duration of the testing.  If you do not do this, your 
   testing may use your existing connections, which would conceal problems.

6. Thoroughly test your access to your hosts.  If you lose access, you can use 
   use either existing connections or your original ssh-agent to regain access.

SEE ALSO
========

avendesora
sshconfig


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
