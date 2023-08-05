# -*- coding: UTF-8 -*-

def f2x(filepath):
	"""
	file to \x
	worked all python version
	"""
    import os
    result = b""
    with open(filepath, "rb") as f:
        for _ in range(os.path.getsize(filepath)):
            item = str(hex(ord(f.read(1))))
            item = r"\x" + item[2:]
            result += item
    return result