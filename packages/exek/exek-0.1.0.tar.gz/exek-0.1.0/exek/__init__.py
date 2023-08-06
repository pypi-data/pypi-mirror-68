from typing import Union, IO
import subprocess
from subprocess import PIPE
import sys
from typing import Sequence, Any, Mapping, Callable, Tuple, IO, Optional, Union, Type, Generic, TypeVar, AnyStr, overload

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

_FILE = Union[None, int, IO[Any]]
_TXT = Union[bytes, str]
if sys.version_info >= (3, 6):
    from os import PathLike
    _PATH = Union[bytes, str, PathLike]
else:
    _PATH = Union[bytes, str]
_CMD = Union[_PATH, Sequence[_PATH]]
_ENV = Union[Mapping[bytes, _TXT], Mapping[str, _TXT]]



# Methods on exek:
# popen: subprocess.Popen(...), with all the magic sauce for pipes, cmd, stderr in
# exceptions, etc.
# run: popen(...).wait() with expectcode handling
# read: run(..., stderr=PIPE, stdout=PIPE).stdout
# check: run(..., expectcode=None).returncode == 0
# cmd: store args but don't run
#   - can pass into in/out/err for piping
#   - can pass into run/read/check for reusable commands

# Methods on class Popen:
# unsafe_io: object containing stdout, stderr, and stdin. These are unsafe when more
# than one is a pipe, so we discourage their use by putting them here. All common use
# cases should be handled by higher level methods anyway.
# iter: method on popen object that returns line iterator with safe handling of pipe
#   buffers if stderr or stdin are pipes (it does a select, storing stderr data
#   elsewhere)

class Cmd:
    def __init__(self):
        pass

def popen(
    command: Union[str, Cmd],
    *args: str,
    bufsize=-1,
    executable=None,
    stdin=None,
    stdout=None,
    stderr=None,
    preexec_fn=None,
    close_fds=True,
    shell=False,
    cwd=None,
    env=None,
    universal_newlines=None,
    startupinfo=None,
    creationflags=0,
    restore_signals=True,
    start_new_session=False,
    pass_fds=(),
    encoding=None,
    errors=None,
    text=None
):
    pass

def run(*args):
    pass

def read(*args):
    pass

def check(*args):
    pass

def cmd(*args):
    pass
