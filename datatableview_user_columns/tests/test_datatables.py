from django import test
from django.contrib.auth import get_user_model

from datatableview_user_columns.datatables import DataTableUserDataTableMixin
from datatableview_user_columns.models import DataTableUserColumns
User = get_user_model()

class DataTablesTestCase(test.TestCase):

    def test_init(self):
        user = User.objects.create_user("Nadia")
        sls = DataTableUserDataTableMixin(table_name="test_table", user=user)
        self.assertEqual(sls.table_name, "test_table")
        self.assertEqual(user.username, "Nadia")
        print(sls)


    def test_column_edit_url(self):
        user = User.objects.create_user("Nadia")
        sls = DataTableUserDataTableMixin(table_name="test_table", user=user)
        self.assertEqual(sls.column_edit_url(), "/datatables/test_table/edit/")
        print(sls.column_edit_url)
