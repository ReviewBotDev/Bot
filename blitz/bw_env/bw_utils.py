# coding=utf8
import re
import os

from constants import BW_SCRIPTS

def get_processes(text, process_name):
    return [p.encode('ascii', 'ignore') for p in re.findall("{}\d+".format(process_name), text)]


def get_data_by_marker(mark, text):
    pattern = '{} >[\w, \[\]]+<'.format(mark.replace('[', '\[').replace(']', '\]'))
    r = re.findall(pattern, text)
    if r:
        s = r[0]
        l, r = s.index('>'), s.index('<')
        data = s[l+1:r]
        return eval(data)


def get_bw_script(path):
    return os.path.join(BW_SCRIPTS, path)



__all__ = [
    'get_processes',
    'get_data_by_marker',
    'get_bw_script',
]