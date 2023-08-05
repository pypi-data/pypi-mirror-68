# -*- coding: utf-8 -*-
"""
Created on Sun May 10 01:25:46 2020

@author: yoelr
"""
import os
import json

__all__ = ('load_json',)

def load_json(folder, json_file, hook=None):
    with open(os.path.join(folder, json_file)) as f:
        return json.loads(f.read(), object_hook=hook)