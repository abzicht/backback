#!/usr/bin/python3
import sys, os
import logging

try:
    from backback.config import Config
    from backback.deja import Deja
    from backback.duplicity import Duplicity
    from backback.manual import Manual
    from backback.remote import Remote
    from backback.local import Local
    from backback.shell import Rankshell 
    from backback.util import prompt_
except ImportError:
    from config import Config
    from deja import Deja
    from duplicity import Duplicity
    from manual import Manual
    from remote import Remote
    from local import Local
    from shell import Rankshell 
    from util import prompt_

logging.basicConfig(level=logging.INFO, format='%(asctime)s (%(levelname)s): %(message)s')

def main():
    """
    This function is being called by the console command backback
    """
    # find out what the user wants to do by prompting for config
    c = Config.init()
    if c.deja:
        Rankshell.add(Deja(c.d['dejadup']))
    if 'local' in c.d:
        for entry in c.d['local']:
            local = Local.init(entry)
            Rankshell.add(local)
    if 'manual' in c.d:
        for entry in c.d['manual']:
            manual = Manual.init(entry)
            Rankshell.add(manual)
    if c.duplicity:
        if 'duplicity' in c.d:
            for entry in c.d['duplicity']:
                duplicity = Duplicity.init(entry, c.duplicity_passphrase)
                Rankshell.add(duplicity)
    if c.remote:
        if 'remote' in c.d:
            for entry in c.d['remote']:
                remote = Remote.init(entry, c.ssh_passphrase)
                Rankshell.add(remote)

    # prompt the user with the specified backup plan and
    # ask whether backup execution should start
    print(Rankshell.verbose_list())
    start_ = prompt_('Start backup?', default=True)
    if not start_:
        return
    logging.info("Starting backup")
    Rankshell.execute()

if __name__ == '__main__':
    main()

