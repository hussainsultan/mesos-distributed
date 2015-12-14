## Setup (OS X)

- install mesos via brew
```
brew install mesos
```

- add mesos python package to site-packages
```
echo 'import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")' >> $HOME/lib/python2.7/site-packages/homebrew.pth
```
- make sure your hostname is added to ```/etc/hosts``` file ```127.0.0.1 HOSTNAME in your /etc/hosts```