# -*- coding: utf-8 -*-
import base64


def encode(data, *args, **kwargs):
    return base64.standard_b64encode(data).decode("UTF-8")
