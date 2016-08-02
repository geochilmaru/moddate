from distutils.core import setup
import py2exe

excludes = [
    "pywin",
    "pywin.debugger",
    "pywin.debugger.dbgcon",
    "pywin.dialogs",
    "pywin.dialogs.list",
    "win32com.server",
]

#options = {
#    "bundle_files": 1,                 # create singlefile exe
#    "compressed"  : 1,                 # compress the library archive
#    "excludes"    : excludes,
#    "dll_excludes": ["w9xpopen.exe"]   # we don't need this
#}

setup(
    options = {"py2exe": {"packages": ["encodings"],"bundle_files": 1}},
    zipfile = None,
    console = ["moddate.py"]
)