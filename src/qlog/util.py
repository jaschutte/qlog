
import sys
import re
import os
import unicodedata
import subprocess
import sys
from colorama import Fore, Style, just_fix_windows_console

just_fix_windows_console()

WORKING_DIR = os.getcwd()

# fancy output
def red(s):
    if sys.stderr.isatty() and "NO_COLOR" not in os.environ:
        return f"{Fore.RED}{s}{Style.RESET_ALL}"
    return s
def yellow(s):
    if sys.stderr.isatty() and "NO_COLOR" not in os.environ:
        return f"{Fore.YELLOW}{s}{Style.RESET_ALL}"
    return s
def emph(s):
    if sys.stderr.isatty() and "NO_COLOR" not in os.environ:
        return f"{Style.BRIGHT}{s}{Style.RESET_ALL}"
    return s


# error handling
ERROR = False
WARN = False

def error(msg = None):
    global ERROR
    ERROR = True

    if msg:
        eprint(red("ERROR: ")+msg)

def fatal(msg = None):
    error(msg)
    smart_exit(1)

def warn(msg):
    global WARN
    WARN = True
    eprint(yellow("WARN: ")+msg)

def has_failed():
    return ERROR

def smart_exit(always=True):
    if has_failed():
        eprint(red("Program finished with errors"))
        exit(1)
    if always:
        if WARN:
            eprint(yellow("Program finished with warnings"))
        exit(0)

# custom assert
def assertt(cond,msg):
    if not cond:
        fatal(msg)


# print to stderr
def eprint(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

# remove special characters, make upper case (a tad overkill, but it works well)
def clean_string(s):
    return re.sub(r"\W+","",
                  unicodedata.normalize("NFD",s)
                     .encode("ascii","ignore")
                     .decode("utf-8")
                     .upper().replace("-","_")
                     .replace(" ","_")
                     .replace("\n","_")
                  ).strip("_").replace("__","_").replace("__","_")



# indent with a leading dash and no spaces on newlines, and no trailing newline
def item(b):
    return "- " + re.sub(r"^\s+$", "", b.replace("\n","\n  "), re.MULTILINE).rstrip()


# find a git repo root dir
def root_dir(CONFIG_FILE):
    # try finding the config locally first
    if os.path.exists(CONFIG_FILE):
        return
    # else, try the git root dir
    result = subprocess.run("git rev-parse --show-toplevel".split(), capture_output=True)
    if result.returncode:
        pass
    else:
        git_root = result.stdout.decode().strip()
        if os.path.exists(os.path.join(git_root,CONFIG_FILE)):
            os.chdir(git_root)
