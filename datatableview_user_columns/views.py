# -*- coding: utf-8 -*-
"""views.py: Django """

from __future__ import unicode_literals
from __future__ import print_function

import importlib
import logging
import os
import inspect

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

from .datatables import DataTableUserColumnsDataTable
from datatableview import views
from .forms import UserColumnsUpdateForm, UserColumnsForm
from .models import DataTableUserColumns
from django.views.generic import CreateView, DeleteView, ListView

__author__ = "Steven Klass"
__date__ = "8/10/17 11:41"
__copyright__ = "Copyright 2017 IC Manage. All rights reserved."
__credits__ = [
    "Steven Klass",
]

log = logging.getLogger(__name__)

try:
    from apps.core.views.generics import AuthenticationMixin
except ModuleNotFoundError:
    log.warning("No auth mixin found!")

    class AuthenticationMixin(object):
        pass


try:
    from apps.core.views.generics import IPCUpdateView as UpdateView
except ModuleNotFoundError:
    from django.views.generic import UpdateView


try:
    from apps.core.views.generics import IPCDatatableView as DatatableMixin
except ModuleNotFoundError:
    log.warning("No IPC Datatable view found!")

    class DatatableMixin(object):
        def get_datatable_kwargs(self, **kw):
            return {}


class DataTableUserMixin(DatatableMixin):
    def get_datatable_kwargs(self, **kwargs):
        kwargs = super(DataTableUserMixin, self).get_datatable_kwargs(**kwargs)
        kwargs["user"] = None
        if hasattr(self, "request"):
            kwargs["user"] = self.request.user
        kwargs["table_name"] = self.get_table()
        return kwargs

    def get_table(self):
        filename = inspect.getfile(self.__class__)
        package = os.path.basename(os.path.dirname(filename))
        module = os.path.splitext(os.path.basename(filename))[0]
        return ".".join([package, module, self.__class__.__name__])


class DataTableUserColumnsCreateView(AuthenticationMixin, CreateView):
    form_class = UserColumnsForm
    template_name = "datatableview_user_columns/datatableusercolumns_form.html"

    def get_queryset(self):
        return DataTableUserColumns.objects.all()

    def get(self, request, *args, **kwargs):
        # This is simply a flag to create a dummy holder.
        # The create happens on the get (which is wrong)

        # Table name is a reference to the list view for a given table
        _import = ".".join(kwargs.get("table_name").split(".")[:-1])
        _class = kwargs.get("table_name").split(".")[-1]

        i = importlib.import_module(_import, [_class])
        datatable_class = getattr(i, _class).datatable_class

        obj, create = DataTableUserColumns.objects.get_or_create(
            user=request.user,
            table_name=kwargs.get("table_name"),
            defaults={"columns": ",".join(datatable_class.default_columns)},
        )

        next_page = self.request.GET.get("next", "")
        if len(next_page):
            next_page = "?next=" + next_page

        return HttpResponseRedirect(
            reverse("user_columns:update", kwargs=dict(pk=obj.id)) + next_page
        )


class DataTableUserColumnsUpdateView(UpdateView):
    form_class = UserColumnsUpdateForm

    def get_queryset(self):
        return DataTableUserColumns.objects.all()

    def get_form_kwargs(self):
        kwargs = super(DataTableUserColumnsUpdateView, self).get_form_kwargs()
        kwargs["choices"] = self.object.get_available_column_choices()
        kwargs["initial"] = {"columns": self.object.columns.split(",")}
        return kwargs

    def get_cancel_url(self):
        return self.request.GET.get("next", "/")

    def get_success_url(self):
        return self.request.GET.get("next", "/")

    def get_context_data(self, **kwargs):
        data = super(DataTableUserColumnsUpdateView, self).get_context_data(**kwargs)
        data["next"] = self.request.GET.get("next")
        data["column_choices"] = [x[1] for x in self.object.get_available_column_choices()]
        data["delete_url"] = reverse("user_table_delete", kwargs=dict(pk=self.object.id))
        return data


class DataTableUserColumnsDeleteView(DeleteView):
    def get_queryset(self):
        return DataTableUserColumns.objects.all()

    def get_success_url(self):
        return self.request.GET.get("next", "/")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class DataTableUserColumnsListView(DataTableUserMixin, ListView):
    permission_required = "ip_verification.view_regressiontagsummary"
    datatable_class = DataTableUserColumnsDataTable
    show_add_button = False

    def get_queryset(self):
        return DataTableUserColumns.objects.all()
