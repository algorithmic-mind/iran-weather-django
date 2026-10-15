from datetime import date, datetime

import jdatetime


PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def jalali_date(value):
    """Convert an ISO Gregorian date to a Persian Jalali date."""
    gregorian = date.fromisoformat(value)
    converted = jdatetime.date.fromgregorian(date=gregorian)
    return f"{converted.year:04d}/{converted.month:02d}/{converted.day:02d}".translate(PERSIAN_DIGITS)


def jalali_datetime(value):
    """Open-Meteo timestamps already use the requested Asia/Tehran timezone."""
    local_time = datetime.fromisoformat(value)
    return f"{jalali_date(local_time.date().isoformat())}، {local_time:%H:%M}".translate(PERSIAN_DIGITS)
