#!/usr/bin/env python
'''Purge old backups'''
# pylint: disable=C0103
# That's about "github-snapshot" isn't a legal module name.
# Requires python 2 for codekit.
# Requires github3 v1.0 for repository iteration.
from __future__ import print_function
import argparse
import os
import os.path
import sys
import datetime
import subprocess
import progressbar


class ReportDir(object):
    '''Class to provide progressbar widget with current directory name.'''

    _current_dir = ''

    def __init__(self):
        pass

    def __call__(self, progress, data):
        return self._current_dir

    def set_directory_name(self, arg):
        '''Set current directory name'''
        self._current_dir = arg

    def get_directory_name(self):
        '''Get current directory name'''
        return self._current_dir


def parse_args():
    '''Parse command-line arguments'''
    parser = argparse.ArgumentParser(
        description="Remove old snapshots")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="enable debugging")
    parser.add_argument("-a", "--access-key", "--aws-access-key",
                        "--aws-access-key-id",
                        help="AWS access key ID [ $AWS_ACCESS_KEY_ID | " +
                        "<from instance metadata> ]")
    parser.add_argument("-s", "--secret-access-key", "--aws-secret-access-key",
                        "--secret-key", "--aws-secret-key",
                        help="AWS secret key [ $AWS_SECRET_ACCESS_KEY | ]" +
                        "<from instance metadata> ]")
    parser.add_argument("-r", "--region", "--default-region",
                        "--aws-default-region",
                        help="AWS default region [ $AWS_DEFAULT_REGION | " +
                        "us-west-2 ]")
    parser.add_argument("-b", "--bucket", "--s3-bucket",
                        help="S3 bucket for storage snapshots" +
                        "[ $S3_BACKUP_BUCKET | lsst-github-backups ]")
    results = parser.parse_args()
    if not results.access_key:
        results.access_key = add_defaults("AWS_ACCESS_KEY_ID")
    if not results.secret_access_key:
        results.secret_access_key = add_defaults("AWS_SECRET_ACCESS_KEY")
    if not results.region:
        results.region = add_defaults("AWS_DEFAULT_REGION")
        if not results.region:
            results.region = "us-west-2"
    if not results.bucket:
        results.bucket = add_defaults("S3_BACKUP_BUCKET",
                                      "lsst-github-backups")
    return results


def add_defaults(envvar, fallback=None):
    '''Set variable default from environment or fallback value'''
    if envvar in os.environ:
        return os.environ[envvar]
    return fallback


def purge_snapshots(args):
    '''Purge snapshots according to retention policy'''
    # The policy is as follows (and maybe we should make this configurable)
    #  1: keep everything for a week.
    #  2: keep any Saturday backup for a month
    #  3: keep any first-of-the-month backup for three months.
    #  4: keep any first-of-the-quarter backup forever (or until manually
    #      deleted)
    #
    # We rely on the fact that the top-level folder name in the bucket is
    #  in ISO 8601 format.
    allsnaps = get_snapshot_dates(args)
    candidates = get_purge_list(allsnaps)
    if not candidates:
        return True
    retval = True
    dirrep = ReportDir()
    pbar = progressbar.ProgressBar(
        widgets=[dirrep, ' | ', progressbar.ETA(), ' ', progressbar.Bar()],
        max_value=len(candidates)).start()
    snapcount = 0
    fnull = open(os.devnull, 'w')
    env = os.environ.copy()
    for snap in candidates:
        dirrep.set_directory_name(snap)
        snapcount += 1
        pbar.update(snapcount)
        cmd = ["aws", "s3", "rm", "--recursive", "s3://" + args.bucket +
               "/" + snap]
        sp1 = subprocess.Popen(cmd, env=env, stdin=fnull, stdout=fnull)
        sp1.wait()
        if sp1.returncode != 0:
            retval = False
    return retval


def get_snapshot_dates(args):
    '''Get set of dates from S3 folder names'''
    env = os.environ.copy()
    cmd = ["aws", "s3", "ls", "s3://" + args.bucket]
    sp1 = subprocess.Popen(cmd, env=env, stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (sod, sed) = sp1.communicate()
    if sed:
        print(sed, file=sys.stderr)
    rawoutlines = sod.split("\n")
    strippedoutlines = [x.strip() for x in rawoutlines]
    filteredoutlines = [x[4:-1] for x in strippedoutlines if
                        x[:4] == "PRE "]
    ymdtuples = []
    for filt in filteredoutlines:
        ymdtextlist = filt.split('-')
        if len(ymdtextlist) == 3:
            # It's a plausible candidate
            try:
                ymdlist = [int(x) for x in ymdtextlist]
                ymdtuples.append(tuple(ymdlist))
            except ValueError:
                # But it wasn't a date
                pass
    return ymdtuples


def get_purge_list(snapdates):
    '''Apply policy to determine which snapshots to purge'''
    purgelist = []
    today = datetime.date.today()
    for dtuple in snapdates:
        sdate = datetime.date(year=dtuple[0], month=dtuple[1], day=dtuple[2])
        age = (today - sdate).days
        # Now we implement our policy
        if age < 8:
            continue
        if age < 32:
            if sdate.weekday() == 5:
                # Don't purge Saturday backups for at least a month
                continue
        if sdate.day == 1:
            # Keep first-of-the-month for at least a quarter
            if (sdate.month + 3) > today.month:
                continue
            # Keep quarterlies forever
            if (sdate.month) % 3 == 1:
                continue
        # This one can go
        purgelist.append(sdate.isoformat())
    return purgelist


def main():
    '''Main entry point'''
    args = parse_args()
    retval = purge_snapshots(args)
    if not retval:
        sys.exit(1)

if __name__ == "__main__":
    main()
