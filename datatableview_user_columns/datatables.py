# -*- coding: utf-8 -*-
"""datatables.py: Django """

from __future__ import unicode_literals
from __future__ import print_function

import logging
from collections import OrderedDict

from datatableview import datatables
from django.core.urlresolvers import reverse

from .models import DataTableUserColumns

__author__ = 'Steven Klass'
__date__ = '8/10/17 13:17'
__copyright__ = 'Copyright 2017 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)


class DataTableUserDataTableMixin(object):
    default_columns = []

    def __init__(self, user=None, table_name=None, *args, **kwargs):
        super(DataTableUserDataTableMixin, self).__init__(*args, **kwargs)
        keep_columns = self.default_columns
        self.table_name = table_name
        self.column_datatable_object = None
        if user and table_name:
            try:
                self.column_datatable_object = DataTableUserColumns.objects.get(user=user, table_name=table_name)
            except DataTableUserColumns.DoesNotExist:
                pass
            else:
                keep_columns = self.column_datatable_object.columns.split(',')

        if hasattr(self, 'required_columns'):
            keep_columns = [k for k in keep_columns if k not in [x[1] for x in self.required_columns]]
            for (k, pos) in self.required_columns:
                keep_columns.insert(pos, k)
        self.columns = OrderedDict([(k, self.columns.get(k)) for k in keep_columns])

    @property
    def column_edit_url(self):
        if self.table_name:
            if self.column_datatable_object is None:
                return reverse('user_table_create', kwargs=dict(table_name=self.table_name))
            else:
                return reverse('user_table_update', kwargs=dict(pk=self.column_datatable_object.id))

    @property
    def column_delete_url(self):
        if self.table_name and self.column_datatable_object:
            return reverse('user_table_delete', kwargs=dict(pk=self.column_datatable_object.id))


#
# Example

#

class DataTableUserColumnsDataTable(DataTableUserDataTableMixin, datatables.Datatable):
    pk = datatables.IntegerColumn("PK", sources=['pk'])
    username = datatables.TextColumn("Username", sources=['user__username'])
    email = datatables.TextColumn("Email", sources=['user__email'])
    table = datatables.TextColumn("Table", sources=['table_name'])
    columns = datatables.TextColumn("Columns", sources=['columns'])
    last_updated = datatables.DateTimeColumn("Last Updated", sources=['last_updated'])

    default_columns = ['username', 'table', 'columns']  # This lists out the default set of columns for a user
    required_columns = [('pk', 0)]                      # This says that at position 0 no matter what show pk

    class Meta:
        model = DataTableUserColumns
        columns = [
            'pk',
            'username',
            'email',
            'table',
            'columns',
            'last_updated',
        ]
