# -*- coding: utf-8 -*-
from django import test
from django.contrib.auth import get_user_model

from datatableview_user_columns.models import DataTableUserColumns

User = get_user_model()


class TestUserColumns(test.TestCase):
    def test_ToString(self):
        user = User.objects.create_user("Nadia")
        obj = DataTableUserColumns.objects.create(user=user, table_name="test.col")
        self.assertEqual(str(obj), "DataTableUserColumns object (1)")
        print(obj)

    def test_get_datatable_class(self):
        user = User.objects.create_user("Nadia")
        obj = DataTableUserColumns.objects.create(
            user=user,
            table_name="datatableview_user_columns.views.DataTableUserColumnsListView",
        )
        self.assertEqual(
            obj.get_datatable_class().__name__, "DataTableUserColumnsDataTable"
        )
        print(obj.get_datatable_class())

    def test_get_available_column_choices(self):
        user = User.objects.create_user("Nadia")
        obj = DataTableUserColumns.objects.create(
            user=user,
            table_name="datatableview_user_columns.views.DataTableUserColumnsListView",
        )
        self.assertEqual(
            obj.get_available_column_choices(),
            [
                ("pk", "PK"),
                ("username", "Username"),
                ("email", "Email"),
                ("table", "Table"),
                ("columns", "Columns"),
                ("last_updated", "Last Updated"),
            ],
        )
