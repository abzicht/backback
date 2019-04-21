#!/usr/bin/python3
import sys, os
from prompt_toolkit import prompt

try:
    from backback.config import Config
    from backback.deja import Deja
    from backback.remote import Remote
    from backback.local import Local
except ImportError:
    from config import Config
    from deja import Deja
    from remote import Remote
    from local import Local

def main():
    """
    This function is being called by the console command backback
    """
    # find out what the user wants to do by prompting for config
    c = Config.init()
    # fill this list with scheduled backup procedures
    backup_procedures = []
    if c.deja:
        # put deja on the first place so that its output can be combined
        # with local and remote
        backup_procedures.append(Deja())
    # put local rsyncs after deja
    for entry in c.d['local']:
        local = Local(entry['from'], entry['to'])
        backup_procedures.append(local)
    # finally, add all remote rsyncs
    for name in c.d['remote']:
        entry = c.d['remote'][name]
        remote = Remote(user       = entry['user'],
                        address    = entry['address'],
                        passphrase = c.passphrase, # passphrase of ~/.ssh/id_rsa or similar
                        folders    = entry['folders'],
                        target     = entry['internal'],
                        port       = entry['port'] if 'port' in entry else 22
                       )
        backup_procedures.append(remote)
        # if an external dir is defined as well, rsync the local copy to it after
        # remote rsync is finished
        if c.external and 'external' in entry:
            local = Local(entry['internal'], entry['external'])
            backup_procedures.append(local)

    # prompt the user with the specified backup plan and
    # ask whether backup execution should start
    # output could look like this:
    """
    ┌ 1 DEJA
    ├ 2 LOCAL: /run/media/usr/backup/foo -> /run/media/usr/ext_hdd/foo
    ├ 3 REMOTE: ['/var/www', '/home/pi'] -> /run/media/usr/backup/remote-1/
    └ 4 LOCAL: /run/media/usr/backup/remote-1/ -> /run/media/ruhe/ext_hdd/remote-1/
    """
    print("Scheduling the following list of backup procedures:")
    for i, procedure in enumerate(backup_procedures):
        char = '├'
        if i == 0:
            char = '┌'
        if i == len(backup_procedures) - 1:
            char = '└'
        print(char, i+1, procedure)
    start_ = prompt('Start backup? (Y/n) ')
    start_ = True if len(start_) == 0 or start_.lower() == 'y' else False
    if not start_:
        return
    print("Starting backup")
    for i, procedure in enumerate(backup_procedures):
        char = '├'
        if i == 0:
            char = '┌'
        if i == len(backup_procedures) - 1:
            char = '└'
        print(char, i+1, "Running {}".format(procedure))
        output, err = procedure.backup()
        if err != None and err != 0 and len(err)!=0:
            print("""
Backup procedure {} threw the following error: \x1b[1;2;52;52;52m{}\x1b[0m""".format(i+1, err))
        if output is not None and len(output) != 0:
            print(output)

if __name__ == '__main__':
    main()
