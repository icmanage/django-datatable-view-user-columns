# -*- coding: utf-8 -*-
from django import test
from django.test import TestCase
from django.contrib.auth import get_user_model

from datatableview_user_columns.forms import UserColumnsUpdateForm
from datatableview_user_columns.models import DataTableUserColumns

User = get_user_model()


class TestUserColumnsUpdateForm(TestCase):
    def test_init(self):
        choices = [("col1", "Column 1"), ("col2", "Column 2")]
        form = UserColumnsUpdateForm(choices=choices)
        self.assertEqual(form.fields["columns"].choices, choices)

    def test_clean_columns(self):
        form = UserColumnsUpdateForm(self)
        form.cleaned_data = {"columns": ["Column 1", "Column 2"]}
        cleaned_columns = form.clean_columns()
        self.assertEqual(cleaned_columns, "Column 1,Column 2")
