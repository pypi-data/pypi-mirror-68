"""
restd is a REST service that routes incoming data to plugins.
The goal is to provide a lightweight, flexible, and extensible
REST framework manged by service configs
"""
import os
from . import restd
from . import performer


def get_version():
    with open('VERSION') as f:
        version = f.read()
        return version


name = "restd"
__version__ = get_version()
