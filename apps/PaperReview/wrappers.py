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
from __future__ import unicode_literals
import os
from django.apps import apps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Model
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.utils.functional import wraps
from guardian.compat import basestring
from guardian.exceptions import GuardianError
from guardian.utils import get_40x_or_None

def file_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        
        if instance.id:
            filename = '{}<{}>{}'.format(filename, instance.version ,ext)
        
            # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper


def permission_required(perm, lookup_variables=None, **kwargs):

    login_url = kwargs.pop('login_url', settings.LOGIN_URL)
    redirect_field_name = kwargs.pop(
        'redirect_field_name', REDIRECT_FIELD_NAME)
    return_403 = kwargs.pop('return_403', False)
    return_404 = kwargs.pop('return_404', False)
    accept_global_perms = kwargs.pop('accept_global_perms', False)


    if not isinstance(perm, basestring):
        raise GuardianError("First argument must be in format: "
                            "'app_label.codename or a callable which return similar string'")

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            obj = None
            if lookup_variables:
                model, lookups = lookup_variables[0], lookup_variables[1:]
                # Parse model
                if isinstance(model, basestring):
                    splitted = model.split('.')
                    if len(splitted) != 2:
                        raise GuardianError("If model should be looked up from "
                                            "string it needs format: 'app_label.ModelClass'")
                    model = apps.get_model(*splitted)
                elif issubclass(model.__class__, (Model, ModelBase, QuerySet)):
                    pass
                else:
                    raise GuardianError("First lookup argument must always be "
                                        "a model, string pointing at app/model or queryset. "
                                        "Given: %s (type: %s)" % (model, type(model)))
                # Parse lookups
                if len(lookups) % 2 != 0:
                    raise GuardianError("Lookup variables must be provided "
                                        "as pairs of lookup_string and view_arg")
                lookup_dict = {}
                for lookup, view_arg in zip(lookups[::2], lookups[1::2]):
                    if view_arg not in kwargs:
                        raise GuardianError("Argument %s was not passed "
                                            "into view function" % view_arg)
                    lookup_dict[lookup] = kwargs[view_arg]
                obj = get_object_or_404(model, **lookup_dict)

            response = get_40x_or_None(request, perms=[perm], obj=obj,
                                       login_url=login_url, redirect_field_name=redirect_field_name,
                                       return_403=return_403, return_404=return_404, accept_global_perms=accept_global_perms)
            if response:
                return response
            return view_func(request, *args, **kwargs)
        return wraps(view_func)(_wrapped_view)
    return decorator


def permission_required_or_403(perm, *args, **kwargs):

    kwargs['return_403'] = True
    return permission_required(perm, *args, **kwargs)


def permission_required_or_404(perm, *args, **kwargs):


    kwargs['return_404'] = True
    return permission_required(perm, *args, **kwargs)



