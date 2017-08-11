# -*- coding: utf-8 -*-
"""views.py: Django """

from __future__ import unicode_literals
from __future__ import print_function

import logging

import os

import datatables
from .models import DataTableUserColumns

__author__ = 'Steven Klass'
__date__ = '8/10/17 11:41'
__copyright__ = 'Copyright 2017 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)

try:
    from apps.core.views.generics import AuthenticationMixin
except:
    log.warning("No auth mixin found!")
    class AuthenticationMixin(object):
        pass

try:
    from apps.core.views.generics import IPCUpdateView as UpdateView
except:
    from django.views.generic import UpdateView


try:
    from apps.core.views.generics import IPCDatatableView as DatatableMixin
except:
    log.warning("No IPC Datatable view found!")
    from datatables.views import DatatableMixin


class DataTableUserMixin(DatatableMixin):

    def get_datatable_kwargs(self, **kwargs):
        kwargs = super(DataTableUserMixin, self).get_datatable_kwargs(**kwargs)
        kwargs['user'] = self.request.user

        package = os.path.basename(os.path.dirname(__file__))
        module = os.path.splitext(os.path.basename(__file__))[0]
        kwargs['table_name'] = ".".join([package, module, self.__class__.__name__])
        return kwargs


#
# Example using our own system...
#


class DataTableUserColumnsListView(DataTableUserMixin):
    permission_required = 'ip_verification.view_regressiontagsummary'
    datatable_class = datatables.DataTableUserColumnsDataTable
    show_add_button = False


    def get_queryset(self):
        return DataTableUserColumns.objects.all()

class DataTableUserColumnsUpdateView(UpdateView):

    def get_queryset(self):
        return DataTableUserColumns.objects.all()
