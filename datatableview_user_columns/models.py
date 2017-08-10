# -*- coding: utf-8 -*-
"""models.py: Django """

from __future__ import unicode_literals
from __future__ import print_function

import logging

from django.conf import settings
from django.db import models
from django.utils.timezone import now

__author__ = 'Steven Klass'
__date__ = '8/10/17 11:41'
__copyright__ = 'Copyright 2017 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)


class DataTableUserColumns(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='datatable_colums')
    table_name = models.CharField(max_length=128)
    columns = models.TextField()

    last_updated = models.DateTimeField(default=now)

    class Meta:
        permissions = (('view_datatableusercolumns', "View Datatable User Columns"),)

    def save(self, *args, **kwargs):
        self.last_updated = now()
        return super(DataTableUserColumns, self).save(*args, **kwargs)