# -*- coding: utf-8 -*-
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

from django.urls.conf import re_path, include

from django.contrib import admin

import datatableview_user_columns


log = logging.getLogger(__name__)

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^user_columns/",
        include("datatableview_user_columns.urls", namespace="user_columns"),
    ),
]
