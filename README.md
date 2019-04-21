# backback

A very specific tool for backing up things.

Utilizes:

* deja-dup [opt.]
* rsync
* ssh [opt.]
* sshpass [opt.]

```bash
git clone https://github.com/abzicht/backback
cd backback
python setup.py install
```

Before running `backback`, make sure to adjust `~/.backback/config.json` to your
needs. When that is done, run `backback` from the command line:

```bash
backback
```

* backback asks you for the passphrase of your ssh key. If you do not own a ssh key,
skip this step by pressing enter. backback will then ask you for the required
ssh password.
* backback offers the functionality to automatically store remote data to multiple
locations. This comes in handy when data is supposed to also be copied to an
external hdd. backback asks you whether or not to store data to an external hdd.
* backback asks you whether [deja-dup](https://gitlab.gnome.org/World/deja-dup)
should be executed at first. This assumes that deja-dup is installed on your system
