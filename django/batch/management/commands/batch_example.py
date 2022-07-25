from django.core.management.base import BaseCommand
import logging


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):
        print(options['id'])
        print("aaa")
        logging.info(options['id'])
        logging.info("bbb")
