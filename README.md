# backback

A very specific tool for backing up things.

Utilizes:

* deja-dup [opt.]
* duplicity [opt.]
* rsync
* ssh [opt.]
* sshpass [opt.]

```bash
git clone https://github.com/abzicht/backback
cd backback
python setup.py install
```

Before running `backback`, make sure to adjust `~/.backback/config.yml` to your
needs. When that is done, run `backback` from the command line:

```bash
backback
```

* backback asks you whether [deja-dup](https://gitlab.gnome.org/World/deja-dup) or duplicity should be executed.
  This assumes that deja-dup or duplicity is installed on your system.
* backback asks you for the passphrase of your ssh key. If you do not own a ssh key, skip this step by pressing enter.
  backback will then ask you for the required ssh password.

## Features

* Copy local or remote (ssh) directories / files from one location to another via __rsync__
* Use __duplicity__ or __deja-dup__ for archiving
* Fully adjust __duplicity__ options
* Full manual command control with the __manual__ option
