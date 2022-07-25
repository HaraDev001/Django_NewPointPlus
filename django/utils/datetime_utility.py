from enum import IntEnum
from typing import Union
from datetime import date, datetime, timedelta, timezone, time
from dateutil.relativedelta import relativedelta

import time as time_epoch

DATETIME_OR_DATE = Union[datetime, date]

__JST = timezone(timedelta(hours=+9))


class Week(IntEnum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


def __add_hours(origin: DATETIME_OR_DATE, hours: int) -> datetime:
    '''時間を加算する

    指定日時 origin に時間を加算することにより、n 時間後の日時を取得する

    Args:
        origin (datetime型またはdate型): 加算前の基準となる日時.
        hours (int型): 基準日時に加算する時間. +n 時間 または -n 時間.

    Returns:
        datetime型またはdate型: 基準日時に指定の時間を加算後の日時.

    '''
    return origin + relativedelta(hours=hours)


def __add_days(origin: DATETIME_OR_DATE, days: int) -> DATETIME_OR_DATE:
    return origin + relativedelta(days=days)


def __add_weeks(origin: DATETIME_OR_DATE, weeks: int) -> DATETIME_OR_DATE:
    return origin + relativedelta(weeks=weeks)


def __add_months(origin: DATETIME_OR_DATE, months: int) -> DATETIME_OR_DATE:
    return origin + relativedelta(months=months)


def __add_years(origin: DATETIME_OR_DATE, years: int) -> DATETIME_OR_DATE:
    return origin + relativedelta(years=years)


def now() -> datetime:
    '''現在日時（JST）を取得'''

    return datetime.now(tz=__JST)


def today() -> date:
    '''今日を返す'''

    return date.today()


def get_datetime(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0) -> datetime:
    '''任意の日時（JST）を取得'''

    return datetime(year, month, day, hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=__JST)


def get_date(year: int, month: int, day: int) -> date:
    '''任意の年月日を取得'''

    return date(year, month, day)


def get_datetime_hours_later_from(origin: datetime,
                                  hours: int = 1) -> datetime:
    '''基準日時の n 時間後の日時を取得する.

    指定日時 origin に時間を加算することにより、n 時間後の日時を取得する.
    __add_hours関数を呼び出す.

    Args:
        origin (datetime型): 加算前の基準となる日時.
        hours (int型 optional default 1): 基準日時に加算する時間. +n 時間.

    Returns:
        datetime型: 基準日時に指定の時間を加算後の日時.

    '''

    return __add_hours(origin=origin, hours=hours)


def get_datetime_hours_before_from(origin: datetime,
                                   hours: int = 1) -> datetime:
    '''基準日時の n 時間前の日時を取得する.

    指定日時 origin に時間を減算することにより、n 時間前の日時を取得する.
    __add_hours関数を呼び出す.

    Args:
        origin (datetime型): 加算前の基準となる日時.
        hours (int型 optional default 1): 基準日時に加算する時間.
                n 時間 > 0 を与えるが、内部でマイナス値に変換して処理される.

    Returns:
        datetime型: 基準日時に指定の時間を加算後の日時.

    '''

    return __add_hours(origin=origin, hours=-hours)


def get_datetime_days_later_from(origin: DATETIME_OR_DATE,
                                 days: int = 1) -> DATETIME_OR_DATE:
    '''基準日時の n 日後の日時を取得する.

    指定日時 origin に日数を加算することにより、n 日後の日時を取得する.
    __add_days関数を呼び出す.

    Args:
        origin (datetime型またはdate型): 加算前の基準となる日時.
        days (int型 optional default 1): 基準日時に加算する日数. +n 日.

    Returns:
        datetime型またはdate型: 基準日時に指定の日数を加算後の日時.

    '''

    return __add_days(origin=origin, days=days)


def get_before_n_day(origin: date, days: int = 1) -> DATETIME_OR_DATE:
    '''n日前を取得'''

    return __add_days(origin=origin, days=-days)


def get_after_n_week(origin: DATETIME_OR_DATE, weeks: int = 1) -> DATETIME_OR_DATE:
    '''n週間後を取得'''

    return __add_weeks(origin=origin, weeks=weeks)


def get_before_n_week(origin: DATETIME_OR_DATE, weeks: int = 1) -> DATETIME_OR_DATE:
    '''n週間前を取得'''

    return __add_weeks(origin=origin, weeks=-weeks)


def get_after_n_month(origin: DATETIME_OR_DATE, months: int = 1) -> DATETIME_OR_DATE:
    '''n月後を取得'''

    return __add_months(origin=origin, months=months)


def get_before_n_month(origin: DATETIME_OR_DATE, months: int = 1) -> DATETIME_OR_DATE:
    '''n月前を取得'''

    return __add_months(origin=origin, months=-months)


def get_after_n_year(origin: DATETIME_OR_DATE, years: int = 1) -> DATETIME_OR_DATE:
    '''n年後を取得'''

    return __add_years(origin=origin, years=years)


def get_before_n_year(origin: DATETIME_OR_DATE, years: int = 1) -> DATETIME_OR_DATE:
    '''n年前を取得'''

    return __add_years(origin=origin, years=-years)


def get_age(birthdate: DATETIME_OR_DATE, today: DATETIME_OR_DATE = today()) -> int:
    '''年齢を取得'''

    if type(birthdate) == datetime:
        birthdate = birthdate.date()

    if type(today) == datetime:
        today = today.date()

    return relativedelta(today, birthdate).years


def get_first_day_of_month(origin: DATETIME_OR_DATE) -> DATETIME_OR_DATE:
    '''月初を取得'''

    return origin + relativedelta(day=1)


def get_last_day_of_month(origin: DATETIME_OR_DATE) -> DATETIME_OR_DATE:
    '''月末を取得'''

    return origin + relativedelta(day=1, months=1, days=-1)


def get_day_by_weekday(origin: DATETIME_OR_DATE, week: Week) -> DATETIME_OR_DATE:
    '''月曜日を始まりとした、その週における任意の曜日を取得'''

    return origin + relativedelta(days=-abs(origin.weekday() - week))


def get_last_moment_of_day(origin: DATETIME_OR_DATE) -> datetime:
    '''その月の最終時刻を取得'''

    if type(origin) == date:
        origin = to_datetime(origin)
    return origin + relativedelta(months=1, day=1, hour=0, minute=0, second=0, microsecond=0, microseconds=-1)


def to_date(origin: datetime) -> date:
    '''datetimeをdateに変換する'''

    return origin.date()


def to_datetime(origin: date) -> datetime:
    '''dateをdatetime（JST）に変換する'''

    return datetime.combine(origin, time(), tzinfo=__JST)


def to_utc_timestamp(origin: datetime):
    '''与えられた日時の1970/01/01から起算した秒数を取得する.

    指定日時 origin の1970/01/01から起算した秒数を取得する.

    Args:
        origin (datetime型): 1970/01/01から起算した秒数に変換させたい日時.

    Returns:
        float型: 1970/01/01から起算した秒数.

    '''

    return time_epoch.mktime(origin.timetuple())
