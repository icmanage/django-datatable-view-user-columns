# -*- coding: utf-8 -*-
"""urls.py: Django """

from __future__ import unicode_literals
from __future__ import print_function

import logging

from django.conf.urls import url

from .views import DataTableUserColumnsListView, DataTableUserColumnsUpdateView, DataTableUserColumnsCreateView, \
    DataTableUserColumnsDeleteView

__author__ = 'Steven Klass'
__date__ = '8/10/17 11:41'
__copyright__ = 'Copyright 2017 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)

app_name = "user_table"

urlpatterns = [
    url(r'^$', DataTableUserColumnsListView.as_view(), name="list"),
    url(r'^create/(?P<table_name>[A-Za-z0-9_\.]+)/$', DataTableUserColumnsCreateView.as_view(), name="create"),
    url(r'^update/(?P<pk>\d+)/$', DataTableUserColumnsUpdateView.as_view(), name="update"),
    url(r'^delete/(?P<pk>\d+)/$', DataTableUserColumnsDeleteView.as_view(), name="delete"),
]
