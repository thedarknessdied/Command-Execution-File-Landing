# -*- coding: utf-8 -*-
import binascii


def encode(data, *args, **kwargs):
    return  binascii.hexlify(data).decode('ascii')
