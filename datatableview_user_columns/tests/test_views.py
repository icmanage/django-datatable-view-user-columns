from django import test
from django.contrib.auth import get_user_model
from django.urls import reverse

from datatableview_user_columns.models import DataTableUserColumns
from datatableview_user_columns.views import DataTableUserMixin

User = get_user_model()

class DataTableUserColumnsViewTests(test.TestCase):

    def test_get(self):
        user = User.objects.create_user("Nadia")
        self.client.force_login(user)
        response = self.client.get(reverse('datatableview_user_columns:data'))
        self.assertEqual(response.status_code, 200)

