from django import test
from django.contrib.auth import get_user_model

from datatableview_user_columns.models import DataTableUserColumns

User = get_user_model()


class TestUserColumns(test.TestCase):

    def test_ToString(self):
        user = User.objects.create_user("Nadia")
        obj = DataTableUserColumns.objects.create(user=user, table_name="test.col")
        self.assertEqual(str(obj), "col")
        print(obj)

    def test_get_datatable_class(self):
        user = User.objects.create_user("Nadia")
        obj = DataTableUserColumns.objects.create(user=user,
                                                  table_name="datatableview_user_columns.views.DataTableUserColumnsListView",)
        self.assertEqual(obj.get_datatable_class().__name__, "DataTableUserColumnsDataTable")
        print(obj.get_datatable_class())

    def test_get_available_column_choices(self):
        user = User.objects.create_user("Nadia")
        obj = DataTableUserColumns.objects.create(user=user,
                                                  table_name="datatableview_user_columns.views.DataTableUserColumnsListView")
        self.assertEqual(obj.get_available_column_choices(), [(u'pk', u'PK'),
                                                              (u'username', u'Username'),
                                                              (u'email', u'Email'),
                                                              (u'table', u'Table'),
                                                              (u'columns', u'Columns'),
                                                              (u'last_updated', u'Last Updated')])
