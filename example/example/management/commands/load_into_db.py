# -*- coding: utf-8 -*-
# Python imports

# 3rd Party imports

# App imports
from django.core.management import BaseCommand

from example.etl import CsvEtl


class Command(BaseCommand):
    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        CsvEtl.load_from_directory("data/archive")
