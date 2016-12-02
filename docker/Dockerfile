FROM centos:7
MAINTAINER sqre-admin
LABEL version="0.2.0" description="LSST DM/SQuaRE GitHub snapshot tools" \
      name="lsstsqre/github-snapshot"

USER root
RUN yum update -y && \
    yum install -y epel-release && yum repolist && \
    yum install -y git python-pip jq python-devel libffi-devel \
     openssl-devel gcc && \
    curl -s \
    https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh  \
    -o install-git-lfs-repo.sh && \
    bash ./install-git-lfs-repo.sh && \
    yum -y install git-lfs && \
    pip install sqre-github-snapshot && \
    useradd -d /home/snapper -m snapper

USER snapper
WORKDIR /home/snapper
RUN git config --global lfs.batch false && \
    git lfs install
COPY assets/gitconfig .gitconfig
COPY assets/gitcredentials .git-credentials

# You may want to specify some or all of the following environment
#  variables with -e to override

# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_SESSION_TOKEN
# AWS_DEFAULT_REGION
# GITHUB_ORGS
# GITHUB_TOKEN
# S3_BACKUP_BUCKET

# Default command is to do a snapshot
# Use "snapshot-purger" on the docker run command line to run a purge

CMD github-snapshot
