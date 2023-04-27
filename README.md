# backback

`backback` is a very specific tool for backing up things.

It utilizes:

* rsync
* deja-dup [opt.]
* duplicity [opt.]
* ssh [opt.]
* sshpass [opt.]

```bash
git clone https://github.com/abzicht/backback
cd backback
python setup.py install
```

Before running backback, make sure to adjust `~/.backback/config.yml` to your
needs. When that is done, run `backback` from the command line:

```bash
backback
```

`backback` runs only local rsync commands, if not otherwise specified.
Running duplicity, deja-dup, or remote backups requires activation via flags:

```bash
# Run local and remote rsync as well as duplicity:
backback --remote --duplicity
# Run local rsync and deja-dup:
backback --deja-dup
```

If activated, backback asks you for ssh and duplicity passphrases. Those can
be skipped, if not required.

## Features

* Copy local or remote (ssh) directories / files from one location to another via __rsync__
* Use __duplicity__ or __deja-dup__ for archiving
* Fully adjust __duplicity__ options
* Full manual command control with the __manual__ option
