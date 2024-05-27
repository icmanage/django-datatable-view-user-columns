import inspect
import os

from django import test
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from datatableview_user_columns.models import DataTableUserColumns
from datatableview_user_columns.views import DataTableUserMixin, DataTableUserColumnsListView

User = get_user_model()


class DataTableUserColumnsViewTests(test.TestCase):

    def test_get_datatable_kwargs(self, kwargs=None):
        data_table_mixin = DataTableUserMixin()
        kwargs = data_table_mixin.get_datatable_kwargs()
        self.assertEqual(kwargs, kwargs)

    def test_get_table(self):
        data_table_mixin = DataTableUserMixin()
        table_name = data_table_mixin.get_table()
        filename = inspect.getfile(DataTableUserMixin)
        package = os.path.basename(os.path.dirname(filename))
        module = os.path.splitext(os.path.basename(filename))[0]
        expected_table_name = ".".join([package, module, DataTableUserMixin.__name__])
        self.assertEqual(table_name, expected_table_name)


class TestDataTableUserColumnsCreateView(TestCase):
    def test_get(self):
        pass



class TestDataTableUserColumnsUpdateView(TestCase):
    def test_get_queryset(self):
        pass

    def test_get_form_kwargs(self):
        pass

    def test_get_cancel_url(self):
        pass

    def test_get_success_url(self):
        pass

    def test_get_context_data(self):
        pass


class TestDataTableUserColumnsDeleteView(TestCase):
    def test_get_queryset(self):
        pass

    def test_get_success_url(self):
        pass

    def test_get(self, *args, **kwargs):
        pass


class TestDataTableUserColumnsListView(TestCase):
    def test_get_queryset(self):
        self.assertEqual(DataTableUserColumns.objects.get_queryset(), DataTableUserColumns.objects.all())


