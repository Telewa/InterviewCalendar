import datetime
from django.utils import timezone

from apps_dir.accounts.serializers import UserSerializer
import calendar
from django.db import connection
from django.conf import settings

from apps_dir.interview_calendar.models import Period, Reservation


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

def roundTime(self, dt=None, roundTo=60 * 60):
    """Round a datetime object to any time lapse in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt == None: dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


def possible_times(start_date, end_date, estimated_duration=settings.INTERVIEW_DURATION, granularity=60):
    allowed_days = [list(calendar.day_name).index(day) + 1 for day in settings.AVAILABLE_DAYS]

    cursor = connection.cursor()
    sql = '''
              SELECT *
              FROM   generate_series (timestamp %(start_date)s
                                      , timestamp %(end_date)s - interval '%(duration)s minutes'
                                      , interval '%(granularity)sm') h 
              WHERE  EXTRACT(ISODOW FROM h) in %(allowed_days)s
                AND    h::time >= %(start_time)s
                AND    h::time <= %(end_time)s - interval '%(duration)s minutes'
                ;
              '''
    cursor.execute(sql, {'start_date': start_date,
                         'start_time': settings.AVAILABLE_START_TIME,
                         'end_date': end_date,
                         'end_time': settings.AVAILABLE_END_TIME,
                         'duration': estimated_duration,
                         'granularity': granularity,
                         'allowed_days': tuple(allowed_days),
                         })

    slots = [str(row[0]) for row in cursor.fetchall() if row[0] > datetime.datetime.now()]
    return slots



def get_my_slots(current_user):
    # current_user = User.objects.get_by_natural_key("emma")

    periods = Period.objects.filter(
        end_time__gte = datetime.datetime.now() + datetime.timedelta(minutes=settings.INTERVIEW_DURATION),
        user=current_user
    )

    reservations = Reservation.objects.filter(
        user=current_user
    )

    reserved_times = [str(reserved_time.start_time) for reserved_time in reservations]

    available_times = [possible_times(period.start_time, period.end_time) for period in periods]
    flat_list = [item for sublist in available_times for item in sublist]

    from structlog import get_logger

    logger = get_logger(__name__)

    for x in reserved_times:
        logger.info(x)

    # return flat_list
    return [available_time for available_time in flat_list if available_time not in reserved_times]

