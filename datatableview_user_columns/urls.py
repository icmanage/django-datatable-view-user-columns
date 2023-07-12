# -*- coding: utf-8 -*-
"""urls.py: Django """

import logging

from django.urls import path, re_path

from .views import DataTableUserColumnsListView, DataTableUserColumnsUpdateView, DataTableUserColumnsCreateView, \
    DataTableUserColumnsDeleteView

__author__ = 'Steven Klass'
__date__ = '8/10/17 11:41'
__copyright__ = 'Copyright 2017 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)

urlpatterns = [
    path('user_columns/', DataTableUserColumnsListView.as_view(), name="user_table_list"),
    re_path(r'^user_columns/create/(?P<table_name>[A-Za-z0-9_\.]+)/$', DataTableUserColumnsCreateView.as_view(), name="user_table_create"),
    path('user_columns/update/<int:pk>/', DataTableUserColumnsUpdateView.as_view(), name="user_table_update"),
    path('user_columns/delete/<int:pk>/', DataTableUserColumnsDeleteView.as_view(), name="user_table_delete"),
]
