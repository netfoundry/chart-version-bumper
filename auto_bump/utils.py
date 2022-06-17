"""
Utility Package
"""


def increment_patch(version):
    return [version[0], version[1], version[2] + 1]


def increment_minor(version):
    return [version[0], version[1] + 1, version[2]]


def increment_major(version):
    return [version[0] + 1, version[1], version[2]]