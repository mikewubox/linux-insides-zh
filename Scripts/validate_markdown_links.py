#!/usr/bin/env python3

from socket import timeout

import os
import sys
import codecs
import re

import markdown

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

def check_live_url(url):

    result = False
    try:
        ret = urlopen(url, timeout=5)
        result = (ret.code == 200)
    except HTTPError as e:
        print(e, file=sys.stderr)
    except URLError as e:
        print(e, file=sys.stderr)
    except timeout as e:
        print(e, file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)

    return result


def main(path):

    filenames = []
    for (dirpath, dnames, fnames) in os.walk(path):
        for fname in fnames:
            if fname.endswith('.md'):
                filenames.append(os.sep.join([dirpath, fname]))

    urls = []

    for filename in filenames:
        fd = codecs.open(filename, mode="r", encoding="utf-8")
        for line in fd.readlines():
            refs = re.findall(r'(?<=<a href=")[^"]*', markdown.markdown(line))
            for ref in refs:
                if ref not in urls:
                    urls.append(ref)
        fd.close()

    for url in urls:
        if not url.startswith("http"):
            print("markdown file name: " + url)
            continue
        if check_live_url(url):
            print(url, ": Success")
        else:
            print(url, ": Failure")


if __name__ == '__main__':

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Choose one path as the argument")
