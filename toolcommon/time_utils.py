from dateutil import rrule
import datetime

BELARUS_TIMEZONE_DELTA = datetime.timedelta(hours=3)

SECOND = 1
MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7


def get_local_midnight(date):
    return date.replace(hour=0, minute=0, second=0) - BELARUS_TIMEZONE_DELTA


def first_day_part(t):
    """Return timedelta between midnight and `t`."""
    return t - get_local_midnight(t)


def office_time_between(start_datetime, end_datetime):
    """Return the total office time between `a` and `b` as a timedelta object."""

    diff_business_days = len(list(rrule.rrule(
        rrule.DAILY,
        dtstart=start_datetime.date(),
        until=end_datetime.date() - datetime.timedelta(days=1),
        byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))
    )

    total = datetime.timedelta(days=diff_business_days)

    if start_datetime.weekday() < 5:
        total -= first_day_part(start_datetime)
    if end_datetime.weekday() < 5:
        total += first_day_part(end_datetime)
    return total


def get_formatted_duration_from_timedelta(remainder):
    return get_formatted_duration_from_seconds(remainder.total_seconds())


def get_formatted_duration_from_seconds(remainder):
    result_string = u''
    result_string, remainder = append_time_measurement(result_string, remainder, WEEK, u'w')
    result_string, remainder = append_time_measurement(result_string, remainder, DAY, u'd')
    result_string, remainder = append_time_measurement(result_string, remainder, HOUR, u'h')
    result_string, remainder = append_time_measurement(result_string, remainder, MINUTE, u'm')

    if not result_string:
        result_string, remainder = append_time_measurement(result_string, remainder, SECOND, u's')

    return result_string


def append_time_measurement(string, remainder, time_measurement, sign):
    if remainder // time_measurement > 0:
        measurement_value, remainder = divmod(remainder, time_measurement)
        string = append_string(string, u'{0:.0f}{1:s}'.format(measurement_value, sign))

    return string, remainder


def append_string(string, app):
    return u'{0} {1}'.format(string, app)
