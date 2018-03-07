# coding:utf-8
"""
@file:      wrappers
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    05/03/2018 2:24 AM
@description:
            --
"""
import os

def file_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        
        if instance.id:
            filename = '{}<{}>{}'.format(filename, instance.version ,ext)
        
            # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper
