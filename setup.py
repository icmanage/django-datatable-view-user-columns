# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='datatableview_user_columns',
    version='0.1.0',
    description='Django Datatable view user columns',
    long_description=readme,
    author='Steven Klasss',
    author_email='sklass@icmanage.com',
    url='https://github.com/icmanage/django-datatable-view-user-columns',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
)

