import functools
import requests
import lxml.html

from .util import *
from .config import *


@functools.lru_cache(maxsize=None)
def get_issue_title(i):
    result = subprocess.run(C.GH_ISSUE_TITLE_CMD.format(issue=i, project=C.PROJECT), shell=True, capture_output=True)
    if result.returncode:
        err = result.stderr.decode().strip()
        error(err)
        return (err, "ERROR")
    else:
        title = result.stdout.decode().strip()
        ty,title = title.split(maxsplit=1)
        return (title, ty)

@functools.lru_cache(maxsize=None)
def get_prs(digest):
    result = subprocess.run(C.GH_BLAME_CMD.format(commit=digest), shell=True, capture_output=True)
    if result.returncode:
        err = result.stderr.decode().strip()
        error(err)
        return []
    else:
        prs = list(map(int,result.stdout.decode().strip().split()))
        return prs

    # url based - gets rate limited
    # html = requests.get(C.COMMIT_URL.format(project=C.PROJECT,commit=digest)).content
    # try:
    #     doc = lxml.html.fromstring(html)
    # except:
    #     error(f"Could not parse response trying to blame {digest}")
    #     prs = []
    # else:
    #     prs = doc.cssselect(".pull-request > a")
    #     print(prs,html.decode())
    #     prs = list({int(pr.text.strip()[1:]) for pr in prs})
    # return prs
