# -*- coding: utf-8 -*-
import inspect
import os

from datatableview import datatables
from django import test
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.views.generic import ListView

from datatableview_user_columns.datatables import DataTableUserDataTableMixin
from datatableview_user_columns.models import DataTableUserColumns
from datatableview_user_columns.views import (
    DataTableUserMixin,
    DataTableUserColumnsUpdateView,
)

User = get_user_model()


class ExampleUserDataTable(DataTableUserDataTableMixin, datatables.Datatable):
    pk = datatables.IntegerColumn("PK", sources=["pk"])
    username = datatables.TextColumn("Username", sources=["username"])
    email = datatables.TextColumn("Email", sources=["email"])
    is_admin = datatables.TextColumn("Admin", sources=["is_admin"])
    is_superuser = datatables.TextColumn("Super", sources=["is_superuser"])

    default_columns = [
        "username",
        "email",
        "is_admin",
    ]  # This lists out the default set of columns for a user
    required_columns = [("pk", 0)]  # This says that at position 0 no matter what show pk

    class Meta:
        model = DataTableUserColumns
        columns = [
            "pk",
            "username",
            "email",
            "is_admin",
            "is_superuser",
        ]


class ExampleUserListView(DataTableUserMixin, ListView):
    datatable_class = ExampleUserDataTable
    show_add_button = False

    def get_queryset(self):
        return User.objects.all()


2


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
        user = User.objects.create_superuser("nadia", "nadia@home.com", "password")
        self.assertTrue(
            self.client.login(username=user.username, password="password"),
            msg="User %s [pk=%s] is not allowed to login" % (user.username, user.pk),
        )

        url = reverse(
            "user_columns:create",
            kwargs={
                "table_name": "datatableview_user_columns.tests.test_views.ExampleUserListView"
            },
        )

        self.assertEqual(DataTableUserColumns.objects.count(), 0)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DataTableUserColumns.objects.count(), 1)
        data_table_column = DataTableUserColumns.objects.get()
        self.assertEqual(response.url, "/user_columns/update/{}/".format(data_table_column.pk))
        # At this point we have created a DataTableUserColumns that should default to
        # whatever is listed in the datatable.default_columns
        self.assertEqual(data_table_column.user, user)
        self.assertEqual(data_table_column.columns, "username,email,is_admin")

        DataTableUserColumns.objects.all().delete()
        self.assertEqual(DataTableUserColumns.objects.count(), 0)
        # Posting to this URL will not do anything.  This is not good practice.
        response = self.client.post(url, data={"columns": "username,email"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DataTableUserColumns.objects.count(), 0)


class TestDataTableUserColumnsUpdateView(TestCase):
    def test_update(self):
        user = User.objects.create_superuser("nadia", "nadia@home.com", "password")
        self.assertTrue(
            self.client.login(username=user.username, password="password"),
            msg="User %s [pk=%s] is not allowed to login" % (user.username, user.pk),
        )

        url = reverse(
            "user_columns:create",
            kwargs={
                "table_name": "datatableview_user_columns.tests.test_views.ExampleUserListView"
            },
        )

        response = self.client.get(url)
        kwargs = {"columns": "username"}
        response = self.client.post(response.url, data={"columns": "username"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        dt = DataTableUserColumns.objects.get()
        self.assertEqual(dt.columns, "username")

        response = self.client.post(
            reverse("user_columns:update", kwargs={"pk": dt.pk}),
            data={"columns": "username"},
        )
        self.assertEqual(response.status_code, 302)
        dt = DataTableUserColumns.objects.get()
        self.assertEqual(dt.columns, "username")
        # self.assertIsInstance(response.context_data, dict)
        # self.assertEqual(response.context_data['1'], 1337)


class TestDataTableUserColumnsDeleteView(TestCase):
    def test_delete(self):
        user = User.objects.create_superuser("nadia", "nadia@home.com", "password")
        self.assertTrue(
            self.client.login(username=user.username, password="password"),
            msg="User %s [pk=%s] is not allowed to login" % (user.username, user.pk),
        )

        url = reverse(
            "user_columns:create",
            kwargs={
                "table_name": "datatableview_user_columns.tests.test_views.ExampleUserListView"
            },
        )

        response = self.client.get(url)
        kwargs = {"columns": "username"}
        dt = DataTableUserColumns.objects.get()
        response = self.client.delete(reverse("user_columns:delete", kwargs=dict(pk=dt.pk)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class TestDataTableUserColumnsListView(TestCase):
    def test_get_queryset(self):
        self.assertEqual(
            list(DataTableUserColumns.objects.get_queryset()),
            list(DataTableUserColumns.objects.all()),
        )
