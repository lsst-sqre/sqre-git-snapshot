# ![Travis](https://img.shields.io/travis/lsst-sqre/sqre-codekit.svg)

# sqre-git-snapshot

LSST DM SQuaRE github snapshot management tools

## Components

### github-snapshot

Makes mirror clones of all public repositories in the specified
organizations.

### snapshot-purger

Removes old snapshots.  Retention criteria are:

1. Everything is retained for a week.
2. Saturday backups are retained for at least a month.
3. First-of-the-month backups are retained for at least 3 months.
4. First-of-the-quarter backups are never automatically deleted.

## Installation

* In the AWS console:
    * Create a new `t2.micro` (or whatever, but micro's plenty big) in
      `us-west-2` using `ami-d2c924b2`.
    * It needs IAM role `github-snapshot-s3-access`.
    * Give it 30GB of SSD as root (you only really need enough for one
      repository at a time, so more-free-space-than-the-biggest-repository
      is good enough, but you're not charged extra (I think) for 30GB or
      less).
    * SSH is the only port it needs open.
    * Launch it.
    * Associate an EIP with it.
    * (optional) Add a DNS record for that EIP
* Once it comes up, log in as `centos`, and then:
   `sudo -i`  
   `hostnamectl set-hostname ghsnap.lsst.codes # Or whatever you called it`  
   `yum update -y`  
   `yum install -y epel-release && yum repolist`  
   `yum install -y git python-pip python-virtualenvwrapper jq`  
   `yum install -y emacs-nox # If you're not a barbarian`  
   `curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh -o install-git-lfs-repo.sh`  
   Examine `install-git-lfs-repo.sh` until you're sure it's not nefarious.  
   `bash ./install-git-lfs-repo.sh`  
   `yum -y install git-lfs-1.5.2-1.el7.x86_64`  
   Reboot.
* Once it is up again, log in as `centos`, and then:  
   `mkdir Venvs gh-snap git`  
   `cd git`  
   `git clone https://github.com/lsst-sqre/shelltools.git`  
   `cd ../gh-snap`  
   `ln -s ../git/shelltools/lsst-shellfuncs.bash`    
   `cd`  
```bash
cat << 'EOF' >> .bashrc
if [ -f /usr/bin/virtualenvwrapper.sh ] && [ -z "${VIRTUAL_ENV}" ]; then
    WORKON_HOME=${HOME}/Venvs
    export WORKON_HOME
    mkdir -p ${WORKON_HOME}
    source /usr/bin/virtualenvwrapper.sh
fi

if [ -f "${HOME}/gh-snap/lsst-shellfuncs.bash" ]; then
    source "${HOME}/gh-snap/lsst-shellfuncs.bash"
fi
EOF
```
* Log out and back in (as `centos` still).  Then:  
  `mkvirtualenv github-snapshot`  
  `pip install sqre-github-snapshot`  
  `cd gh-snap`  
```bash
cat << 'EOF' > run_as_cronjob
#!/bin/bash
action=$1
case $action in
"purge"|"snap")
	;;
*)
	echo 1>&2 "Action must be 'purge' or 'snap'"
	exit 1
esac

declare -F | grep -q '^declare -f workon$'
rc=$?
if [ ${rc} -ne 0 ]; then
    . ${HOME}/.bashrc
else
    declare -F | grep -q '^declare -f deactivate$'
    rc=$?
    if [ ${rc} -ne 0 ]; then
	. ${HOME}/.bashrc
    fi
fi

if [ -n "${VIRTUAL_ENV}" ]; then
    vname=$(basename "${VIRTUAL_ENV}")
fi
if [ "${vname}" != "github-snapshot" ]; then
    workon github-snapshot
fi

check_github_lfs
set_aws_variables

if [ "${action}" == "purge" ]; then
    snapshot-purger
else
    github-snapshot
fi
EOF
```
* Install cron job:    
   `chmod 0755 run_as_cronjob`  
   set `$EDITOR` if you don't like `vi`  
   `crontab -e`  
   Add the following:  
```
# Take backup snapshots every night at 12:23 AM
# Purge old backups every night at 4:46 AM

23 0 * * * /home/centos/gh-snap/run_as_cronjob snap
46 4 * * * /home/centos/gh-snap/run_as_cronjob purge
```
