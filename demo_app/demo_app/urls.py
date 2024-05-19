"""demo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from django.conf.urls import url

from django.contrib import admin

from datatableview_user_columns.views import DataTableUserColumnsListView, DataTableUserColumnsCreateView, \
    DataTableUserColumnsUpdateView, DataTableUserColumnsDeleteView


log = logging.getLogger(__name__)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user_columns/create/(?P<table_name>[A-Za-z0-9_\.]+)/$', DataTableUserColumnsCreateView.as_view(),
        name="user_table_create"),
    url(r'^user_columns/update/(?P<pk>\d+)/$', DataTableUserColumnsUpdateView.as_view(), name="user_table_update"),
    url(r'^user_columns/delete/(?P<pk>\d+)/$', DataTableUserColumnsDeleteView.as_view(), name="user_table_delete"),
]