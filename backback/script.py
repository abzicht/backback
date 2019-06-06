#!/usr/bin/python3
import sys, os
import logging
from prompt_toolkit import prompt

try:
    from backback.config import Config
    from backback.deja import Deja
    from backback.remote import Remote
    from backback.local import Local
    from backback.shell import Rankshell 
except ImportError:
    from config import Config
    from deja import Deja
    from remote import Remote
    from local import Local
    from shell import Rankshell 

logging.basicConfig(level=logging.INFO)

def main():
    """
    This function is being called by the console command backback
    """
    # find out what the user wants to do by prompting for config
    c = Config.init()
    if c.deja:
        Rankshell.add(Deja(c.d['deja-dup']))
    for entry in c.d['local']:
        local = Local.init(entry)
        Rankshell.add(local)
    for name in c.d['remote']:
        entry = c.d['remote'][name]
        remote = Remote.init(entry, c.passphrase)
        Rankshell.add(remote)
        # if an external dir is defined as well, rsync the local copy to it after
        # remote rsync is finished
        if c.external and 'external' in entry:
            # incr the rank for the external copy so that it is only executed __after__
            # the remote copy is done
            external_rank = entry['rank'] + 1
            local = Local(
                    rank  = external_rank,
                    from_ = entry['internal'],
                    to_   = entry['external']
                    )
            Rankshell.add(local)

    # prompt the user with the specified backup plan and
    # ask whether backup execution should start
    print(Rankshell.verbose_list())
    start_ = prompt('Start backup? (Y/n) ')
    start_ = True if len(start_) == 0 or start_.lower() == 'y' else False
    if not start_:
        return
    logging.info("Starting backup")
    Rankshell.execute()

if __name__ == '__main__':
    main()

