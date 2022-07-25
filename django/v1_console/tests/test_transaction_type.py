import os

from config.test_base import BaseTestCase
from database.models import TransactionCategory


class TransactionTypeTests(BaseTestCase):
    api_name = "Api Transaction Type"
    path_to_folder = os.path.abspath(os.path.dirname(__file__)) + "/testcase/transaction"

    def setUp(self) -> None:
        self.make_data()
        super(TransactionTypeTests, self).setUp()

    # TODO: init data

    @staticmethod
    def make_data():
        TransactionCategory.objects.create(id='07e0ba747dc747e5a5c9fdda70fa4fcd', name='取引種別名 1')
        TransactionCategory.objects.create(id='4a5610116d4a49e28383e83aa0472e5d', name='取引種別名 2')
        TransactionCategory.objects.create(id='f40dac8b8fd54598811c5e088ec443f7', name='取引種別名 3')
