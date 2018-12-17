# coding=utf8
import subprocess
import re

from django.core.cache import cache

from internal import vcs
from internal.vcs import GitInfoData
from internal.svn.command import SvnInfoData


__all__ = [
    'GitInfoData',
    'SvnInfoData',

    'GIT_SERVER_SRC_URL',
    'GIT_SERVER_ENV_URL',
    'CACHE_TIME',

    'Repository',
    'getBranches',
    'getServerSrcBranches',
    'getServerEnvBranches',
]


GIT_SERVER_SRC_URL = 'https://stash-dava.wargaming.net/scm/wotb/server.git'
GIT_SERVER_ENV_URL = 'https://stash-dava.wargaming.net/scm/wotb/env.git'
CACHE_TIME = 60.0


class Repository(object):
    def __init__(self, path, info=None):
        self.path = path
        self.vcs_info = vcs.info(self.path) if info is None else info


def _executeCommand(cmd):
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out


def _doGetBranches(gitUrl):
    cmdOut = _executeCommand('git ls-remote ' + gitUrl)
    lines = cmdOut.split('\n')
    branches = ['trunk', 'master']
    otherBranches = []
    pullReqs = []
    tags = []
    for l in lines:
        l = l.split()
        if len(l) < 2:
            continue
        name = l[1]
        releaseBranch = re.match('refs/heads/(release.+)', name)
        branch = re.match('refs/heads/(.+)', name)
        pullReq = re.match('refs/pull-requests/(\d+)/merge', name)
        tag = re.match('refs/tags/([\d\.]+)', name)

        if releaseBranch:
            branches.append(releaseBranch.group(1))
            continue

        if branch:
            otherBranches.append(branch.group(1))
            continue

        if pullReq:
            pullReqs.append(pullReq.group(1))
            continue

        if tag:
            tags.append(tag.group(1))
            continue

    branches += [b for b in otherBranches if b not in branches]
    pullReqs = sorted(map(int,pullReqs), reverse=True)
    tags = sorted(list(set(tags)), reverse=True, key=lambda x: tuple(map(int, x.split('.'))))

    return branches, pullReqs, tags

def getBranches(gitUrl, forceUpdate = False):
    result = cache.get(gitUrl)
    if result is not None and not forceUpdate:
        return result
    result = _doGetBranches(gitUrl)
    cache.set(gitUrl, result, CACHE_TIME)
    return result


def getServerSrcBranches(*args, **kwargs):
    return getBranches(GIT_SERVER_SRC_URL, *args, **kwargs)


def getServerEnvBranches(*args, **kwargs):
    return getBranches(GIT_SERVER_ENV_URL, *args, **kwargs)