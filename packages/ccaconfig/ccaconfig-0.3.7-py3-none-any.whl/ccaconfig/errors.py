"""
errors module for ccaconfig module
"""
import sys


def formatMsg(fname, e):
    ename = type(exc).__name__
    return f"Error in {funcname}: {ename}: {exc}\n"


def errorExit(fname, e, exitlevel=1):
    msg = formatMsg(fname, e)
    sys.stderr.write(msg)
    # sys.stderr.flush()
    sys.exit(exitlevel)


def errorRaise(fname, e):
    msg = formatMsg(fname, e)
    sys.stderr.write(msg)
    raise (e)


def errorNotify(fname, e):
    msg = formatMsg(fname, e)
    sys.stderr.write(msg)
