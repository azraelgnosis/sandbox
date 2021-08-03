from sys import version_info

if version_info < (3,):
    pass
else:
    unicode = str

STRING_TYPES = (str, unicode)
