from datetime import date, datetime, timedelta, timezone
from django.test import SimpleTestCase
from utils import datetime_utility as util


JST = timezone(timedelta(hours=+9))


class TestDatetimeUtility(SimpleTestCase):

    def test_get_after_n_day(self):
        '''1日後を返す'''

#        actual = util.get_after_n_day(date(2020, 1, 1))
        actual = util.get_datetime_days_later_from(date(2020, 1, 1))
        expect = date(2020, 1, 2)
        self.assertEqual(actual, expect)

    def test_get_after_n_day_leap(self):
        '''閏年を含む1日後を返す'''

#        actual = util.get_after_n_day(date(2020, 2, 28))
        actual = util.get_datetime_days_later_from(date(2020, 2, 28))
        expect = date(2020, 2, 29)
        self.assertEqual(actual, expect)

    def test_get_before_n_day(self):
        '''1日前を返す'''

        actual = util.get_before_n_day(date(2020, 1, 1))
        expect = date(2019, 12, 31)
        self.assertEqual(actual, expect)

    def test_get_before_n_day_leap(self):
        '''閏年を含む1日前を返す'''

        actual = util.get_before_n_day(date(2020, 3, 1))
        expect = date(2020, 2, 29)
        self.assertEqual(actual, expect)

    def test_get_after_n_week(self):
        '''1週間後を返す'''

        actual = util.get_after_n_week(date(2020, 1, 1))
        expect = date(2020, 1, 8)
        self.assertEqual(actual, expect)

    def test_get_after_n_week_leap(self):
        '''閏年を含む1週間後を返す'''

        actual = util.get_after_n_week(date(2020, 2, 25))
        expect = date(2020, 3, 3)
        self.assertEqual(actual, expect)

    def test_get_before_n_week(self):
        '''1週間前を返す'''

        actual = util.get_before_n_week(date(2020, 1, 1))
        expect = date(2019, 12, 25)
        self.assertEqual(actual, expect)

    def test_get_before_n_week_leap(self):
        '''閏年を含む1週間前を返す'''

        actual = util.get_before_n_week(date(2020, 3, 7))
        expect = date(2020, 2, 29)
        self.assertEqual(actual, expect)

    def test_get_after_n_month(self):
        '''1ヶ月後を返す'''

        actual = util.get_after_n_month(date(2020, 1, 1))
        expect = date(2020, 2, 1)
        self.assertEqual(actual, expect)

    def test_get_after_n_month_leap(self):
        '''閏年を含む1ヶ月後を返す'''

        actual = util.get_after_n_month(date(2020, 1, 31))
        expect = date(2020, 2, 29)
        self.assertEqual(actual, expect)

    def test_get_before_n_month(self):
        '''1ヶ月前を返す'''

        actual = util.get_before_n_month(date(2020, 1, 1))
        expect = date(2019, 12, 1)
        self.assertEqual(actual, expect)

    def test_get_before_n_month_leap(self):
        '''閏年を含む1ヶ月前を返す'''

        actual = util.get_before_n_month(date(2020, 3, 31))
        expect = date(2020, 2, 29)
        self.assertEqual(actual, expect)

    def test_get_after_n_year(self):
        '''1年後を返す'''

        actual = util.get_after_n_year(date(2020, 1, 1))
        expect = date(2021, 1, 1)
        self.assertEqual(actual, expect)

    def test_get_after_n_year_leap(self):
        '''閏年を含む1年後を返す'''

        actual = util.get_after_n_year(date(2019, 2, 28))
        expect = date(2020, 2, 28)
        self.assertEqual(actual, expect)

    def test_get_before_n_year(self):
        '''1年前を返す'''

        actual = util.get_before_n_year(date(2020, 1, 1))
        expect = date(2019, 1, 1)
        self.assertEqual(actual, expect)

    def test_get_before_n_year_leap(self):
        '''閏年を含む1年前を返す'''

        actual = util.get_before_n_year(date(2021, 2, 28))
        expect = date(2020, 2, 28)
        self.assertEqual(actual, expect)

    def test_get_age(self):
        '''年齢を返す'''

        actual = util.get_age(date(2000, 1, 1), date(2020, 1, 1))
        expect = 20
        self.assertEqual(actual, expect)

    def test_get_age_leap(self):
        '''閏年を含む年齢を返す'''

        actual = util.get_age(date(2004, 2, 29), date(2021, 2, 28))
        expect = 17
        self.assertEqual(actual, expect)

    def test_get_first_day_of_month(self):
        '''月初を返す'''

        actual = util.get_first_day_of_month(date(2020, 1, 5))
        expect = date(2020, 1, 1)
        self.assertEqual(actual, expect)

    def test_get_first_day_of_month_leap(self):
        '''閏年を含む月初を返す'''

        actual = util.get_first_day_of_month(date(2020, 2, 29))
        expect = date(2020, 2, 1)
        self.assertEqual(actual, expect)

    def test_get_last_day_of_month(self):
        '''月末を返す'''

        actual = util.get_last_day_of_month(date(2020, 1, 1))
        expect = date(2020, 1, 31)
        self.assertEqual(actual, expect)

    def test_get_last_day_of_month_leap(self):
        '''閏年を含む月末を返す'''

        actual = util.get_last_day_of_month(date(2020, 2, 1))
        expect = date(2020, 2, 29)
        self.assertEqual(actual, expect)

    def test_get_day_by_weekday(self):
        '''その週の任意の曜日を返す'''

        actual = util.get_day_by_weekday(date(2020, 1, 1), util.Week.MON)
        expect = date(2019, 12, 30)
        self.assertEqual(actual, expect)

    def test_get_last_moment_of_day(self):
        '''その月の最終時刻を返す'''

        actual = util.get_last_moment_of_day(datetime(2020, 1, 1, 2, 3, 4, 5, tzinfo=JST))
        expect = datetime(2020, 1, 31, 23, 59, 59, 999999, tzinfo=JST)
        self.assertEqual(actual, expect)

    def test_to_date(self):
        '''datetimeからdateに変換する'''

        actual = util.to_date(datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=JST))
        expect = date(2020, 1, 1)
        self.assertEqual(actual, expect)

    def test_to_datetime(self):
        '''dateからdatetimeに変換する'''

        actual = util.to_datetime(date(2020, 1, 1))
        expect = datetime(2020, 1, 1, tzinfo=JST)
        self.assertEqual(actual, expect)
