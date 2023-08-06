from .authkeys import AuthKeys
from .utils import run_sftp, date, to_path, Run
from inform import (
    comment, cull, conjoin, error, fatal, fmt, indent, narrate, os_error, warn,
    Error
)
from avendesora import PasswordGenerator, PasswordError
import pexpect

# Open Avendesora password generator
pw = PasswordGenerator()

# Class that manages the SSH key pairs
class Key:
    def __init__(self, name, data, update, skip, trial_run):
        self.keyname = name
        self.data = data
        self.update = update
        self.skip = skip
        self.trial_run = trial_run
        self.warning = ''
        narrate(name)

    def generate(self):
        comment('    creating key')
        keyname = self.keyname
        data = self.data
        servers = self.data.get('servers', [])

        opts = data['keygen_options']
        account_name = data['avendesora_account']
        if account_name:
            name, _, field = account_name.partition('.')
            account = pw.get_account(name)
            passcode = str(account.get_value(field))
            description = fmt("{keyname} (created {date})")
        else:
            passcode = ''
            self.warning = 'This key is not protected with a passcode!'
            description = fmt("{keyname} (created {date} -- no passcode!)")

            # warn user if they have a key with no passcode and no restrictions
            for server in servers:
                server_data = servers[server]
                restrictions = server_data.get('restrictions')
                if not restrictions:
                    warn(
                        'unprotected key being sent to', server,
                        'without restrictions.'
                    )

        args = ['-C', description, '-f', keyname] + opts.split()
        try:
            comment('    running:', 'ssh-keygen', *args)
            keygen = pexpect.spawn('ssh-keygen', args, timeout=None)
            keygen.expect('Enter passphrase.*: ')
            keygen.sendline(passcode)
            keygen.expect('Enter same passphrase again: ')
            keygen.sendline(passcode)
            keygen.expect(pexpect.EOF)
            keygen.close()
        except pexpect.ExceptionPexpect as e:
            fatal(e)

        # remove group/other permissions from keyfiles
        to_path(keyname).chmod(0o600)
        to_path(keyname + '.pub').chmod(0o600)

    def publish_private_key(self):
        keyname = self.keyname
        data = self.data
        clients = self.data.get('clients', [])
        prov = '.provisional' if self.trial_run else ''

        # copy key pair to remote client
        for client in sorted(clients):
            if self.update and client not in self.update:
                continue
            if client in self.skip:
                continue
            narrate('    publishing key pair to', client)
            client_data = clients[client]

            # delete any pre-existing provisional files
            # the goal here is to leave a clean directory when not trial-run
            try:
                run_sftp(client, [
                    fmt('rm .ssh/{keyname}.provisional'),
                    fmt('rm .ssh/{keyname}.pub.provisional'),
                ])
            except Error as e:
                comment('ignoring:', e)

            # now upload the new files
            try:
                run_sftp(client, [
                    fmt('put -p {keyname} .ssh/{keyname}{prov}'),
                    fmt('put -p {keyname}.pub .ssh/{keyname}.pub{prov}'),
                ])
            except Error as e:
                error(e, culprit=client)

    def gather_public_keys(self):
        comment('    gathering public keys')
        keyname = self.keyname
        data = self.data
        clients = conjoin(self.data.get('clients', []))
        default_purpose = fmt('This key allows access from {clients}.')
        purpose = self.data.get('purpose', default_purpose)
        servers = self.data.get('servers', [])
        prov = '.provisional' if self.trial_run else ''

        # read contents of public key
        try:
            pubkey = to_path(keyname + '.pub')
            key = pubkey.read_text().strip()
        except OSError as e:
            narrate('%s, skipping.' % os_error(e))
            return

        # get fingerprint of public key
        try:
            keygen = Run(['ssh-keygen', '-l', '-f', pubkey], modes='wOeW')
            fields = keygen.stdout.strip().split()
            fingerprint = ' '.join([fields[0], fields[1], fields[-1]])
        except Error as e:
            error(e)
            return

        # contribute commented and restricted public key to the authorized_key 
        # file for each server
        for server in servers:
            if self.update and server not in self.update:
                continue
            if server in self.skip:
                continue
            server_data = servers[server]
            description = server_data.get('description', None)
            restrictions = server_data.get('restrictions', [])
            remarks = [
                indent(t, leader= '# ')
                for t in cull([purpose, description, self.warning, fingerprint])
                if t
            ]

            include_file = server_data.get(
                'remote_include_filename', data['remote_include_filename']
            )
            bypass = server_data.get('bypass')
            authkeys = AuthKeys(server, include_file, bypass, self.trial_run)
            authkeys.add_public_key(keyname, key, remarks, restrictions)

        if not servers:
            warn(
                'no servers specified, you must update them manually.', 
                culprit=keyname
            )
