# -*- coding: utf-8 -*-
"""datatables.py: Django """

from __future__ import unicode_literals
from __future__ import print_function

import logging
from collections import OrderedDict

from datatableview import datatables

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
        if user and table_name:
            try:
                keep_columns = DataTableUserColumns.objects.get(user=user, table_name=table_name).columns.split(',')
            except DataTableUserColumns.DoesNotExist:
                pass
        self.columns = OrderedDict([(k, self.columns.get(k)) for k in keep_columns])

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

    default_columns = ['username', 'table', 'columns']

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
