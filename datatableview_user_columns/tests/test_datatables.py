# -*- coding: utf-8 -*-
from django import test
from django.contrib.auth import get_user_model
from django.urls import reverse

from datatableview_user_columns.datatables import DataTableUserDataTableMixin
from datatableview_user_columns.models import DataTableUserColumns
from datatableview_user_columns.views import DataTableUserColumnsDeleteView

User = get_user_model()


class DataTablesTestCase(test.TestCase):
    # testing new setup function
    def setUp(self):
        self.user = User.objects.create_user(username="Nadia")
        self.table_name = "test_table"
        self.column_obj = DataTableUserColumns.objects.create(
            user=self.user, table_name=self.table_name, columns="username,email,table"
        )

    def tearDown(self):
        self.user.delete()
        self.column_obj.delete()

    def test_init(self):
        # Test case where user and table_name are provided
        sls = DataTableUserDataTableMixin(user=self.user, table_name=self.table_name)
        self.assertEqual(sls.table_name, self.table_name)
        self.assertEqual(self.user.username, "Nadia")
        self.assertIsNotNone(sls.column_datatable_object)
        self.assertEqual(sls.column_datatable_object, self.column_obj)

        # Test case where has_errors is True and column_datatable_object is not None
        DataTableUserColumns.objects.all().delete()  # Clear existing objects
        user = User.objects.create_user(username="John")
        table_name = "test_table"
        # Create an invalid column_datatable_object
        column_obj = DataTableUserColumns.objects.create(
            user=user, table_name=table_name, columns="invalid_column"
        )
        sls = DataTableUserDataTableMixin(user=user)
        self.assertIsNone(sls.table_name)
        self.assertEqual(user.username, "John")
        self.assertIsNone(sls.column_datatable_object)
        # Ensure that the invalid column is removed from the column_datatable_object
        self.assertTrue(DataTableUserColumns.objects.filter(id=column_obj.id).exists())
        column_obj.refresh_from_db()
        self.assertEqual(column_obj.columns, "invalid_column")  # Invalid column should be removed

    def test_column_edit_url(self):
        # Case where column_datatable_object is None
        DataTableUserColumns.objects.all().delete()
        sls2 = DataTableUserDataTableMixin(table_name="test_table", user=self.user)
        self.assertEqual(sls2.column_edit_url, "/user_columns/create/test_table/")

        # Case where column_datatable_object is not None
        sls2 = DataTableUserDataTableMixin(user=self.user, table_name=self.table_name)
        self.assertEqual(sls2.column_edit_url, "/user_columns/create/test_table/")

        # Case where table_name is not provided
        sls2 = DataTableUserDataTableMixin(user=self.user)
        self.assertIsNone(sls2.column_edit_url)

    def test_column_delete_url(self):
        # Case when both table_name and column_datatable_object are provided
        sls3 = DataTableUserDataTableMixin(user=self.user, table_name=self.table_name)
        self.assertEqual(sls3.column_delete_url, "/user_columns/delete/1/")
