
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
        obj = DataTableUserColumns.objects.create(user=user, table_name="datatableview_user_columns.views.DataTableUserColumnsListView")
        self.assertEqual(obj.get_datatable_class().__name__, "DataTableUserColumnsDataTable")
        print(obj.get_datatable_class())
