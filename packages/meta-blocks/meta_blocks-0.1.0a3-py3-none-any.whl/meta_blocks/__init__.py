import os

# Get __version__ from version.py.
__version__ = None
ver_file = os.path.join(__path__[0], "version.py")
with open(ver_file) as fp:
    exec(fp.read())
