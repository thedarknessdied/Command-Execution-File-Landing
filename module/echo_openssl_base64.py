# -*- coding: utf-8 -*-

module_echo = """echo {data}>> {src_filename}\n"""
module_certuil = """openssl.exe enc -base64 -d -in  .\\{src_filename} -out .\\{dst_filename}\n"""
src_filename = ""
dst_filename = ""


def run(data, utils, end: bool, *args, **kwargs):
    global src_filename, dst_filename
    if src_filename is None or not src_filename or not isinstance(src_filename, str):
        src_filename = utils.get_random_system().get_random_filename(length=5)
    if dst_filename is None or not dst_filename or not isinstance(dst_filename, str):
        dst_filename = utils.get_factory().get_src_filename()
    tmp = module_echo.format(data=data, src_filename=dst_filename)
    if end:
        tmp += module_certuil.format(src_filename=dst_filename, dst_filename=src_filename)
    return tmp
