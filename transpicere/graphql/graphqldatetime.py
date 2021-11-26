from datetime import date, datetime, time
from math import modf, floor
from typing import Any

from dateutil.parser import parse as dateutil_parse
from dateutil.tz import tzutc

from graphql.error import GraphQLError
from graphql.pyutils import inspect
from graphql.type import GraphQLScalarType

DEFAULT_TIMEZONE = tzutc()


def serialize_datetime(output_value: datetime) -> str:
    return output_value.isoformat()


def parse_datetime(input_value: Any) -> datetime:
    try:
        if isinstance(input_value, datetime):
            return input_value
        elif isinstance(input_value, date):
            return datetime(input_value.year, input_value.month, input_value.day)
        elif isinstance(input_value, float) or isinstance(input_value, int):
            return datetime.fromtimestamp(float(input_value), tz=DEFAULT_TIMEZONE)
        elif isinstance(input_value, str):
            return dateutil_parse(input_value)
        raise ValueError(
            f"Datetime cannot represent non datetime value: {inspect(input_value)}")
    except ValueError:
        raise GraphQLError(
            f"Datetime cannot represent non datetime value: {inspect(input_value)}")


GraphQLDatetime = GraphQLScalarType(
    name="Datetime",
    description="The `Datetime` scalar type represents"
    " non-fractional signed whole numeric values."
    " Int can represent values between -(2^31) and 2^31 - 1.",
    serialize=serialize_datetime,
    parse_value=parse_datetime
)


def serialize_date(output_value: date) -> str:
    return output_value.isoformat()


def get_date(d: datetime) -> date:
    t = d.time().replace(tzinfo=None)
    if t.hour == 0 and t.minute == 0 and t.second == 0 and t.microsecond == 0:
        return d.date()
    print(f"{d.isoformat()} {t} : {d.hour}:{d.minute}:{d.second}.{d.microsecond}")
    raise ValueError()


def parse_date(input_value: Any) -> date:
    if isinstance(input_value, datetime):
        return input_value.date()
    elif isinstance(input_value, date):
        return input_value

    try:
        d = parse_datetime(input_value)
        return get_date(d)
    except (GraphQLError, ValueError):
        raise GraphQLError(
            f"Date cannot represent non date value: {inspect(input_value)}")


GraphQLDate = GraphQLScalarType(
    name="Date",
    description="The `Date` scalar type represents"
    " non-fractional signed whole numeric values."
    " Int can represent values between -(2^31) and 2^31 - 1.",
    serialize=serialize_date,
    parse_value=parse_date,
)


def serialize_time(output_value: time) -> str:
    return output_value.isoformat()


def parse_time(input_value: Any) -> time:
    if isinstance(input_value, time):
        return input_value
    elif isinstance(input_value, int):
        s = floor(input_value % 60)
        m = floor(((input_value - s) / 60) % 60)
        h = floor((input_value - s - 60*m)/(60*60))
        return time(h, m, s)
    elif isinstance(input_value, float):
        sub_seconds, seconds = modf(input_value)
        t = parse_time(int(seconds))
        return time(t.hour, t.minute, t.second, floor(sub_seconds*1000000))
    elif isinstance(input_value, str):
        return time.fromisoformat(input_value)
    else:
        raise GraphQLError(
            f"Date cannot represent non date value: {inspect(input_value)}")


GraphQLTime = GraphQLScalarType(
    name="Time",
    description="The `Date` scalar type represents"
    " non-fractional signed whole numeric values."
    " Int can represent values between -(2^31) and 2^31 - 1.",
    serialize=serialize_time,
    parse_value=parse_time)
