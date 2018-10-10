# Models

## Install and uninstall
### Installing R in ubuntu 16

```
sudo apt-get install r-base --yes
```


### Installing irace

```
sudo R CMD INSTALL irace
```

Add the following to .zshrc or .bashrc
```
# Irace path
# Path given by system.file(package="irace")
export IRACE_HOME=/usr/local/lib/R/site-library/irace
export PATH=${IRACE_HOME}/bin/:$PATH
```
