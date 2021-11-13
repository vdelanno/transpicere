import pytest
from decimal import Decimal
from transpicere.graphql.graphqldatetime import (
    parse_datetime, GraphQLDatetime, GraphQLDate, GraphQLTime, GraphQLError)
from scalar_schema import check_scalar_schema
import sys
from datetime import datetime, date, time
from dateutil.tz import tzutc


@pytest.mark.parametrize("input_value,inner_value", [
    ("Thu Sep 25 10:36:28 2003", datetime(2003, 9, 25, 10, 36, 28)),
    ("Thu Sep 25 2003", datetime(2003, 9, 25)),
    ("2003-09-25T10:49:41", datetime(2003, 9, 25, 10, 49, 41)),
    ("2003-09-25T10:49", datetime(2003, 9, 25, 10, 49)),
    ("2003-09-25T10", datetime(2003, 9, 25, 10)),
    ("2003-09-25", datetime(2003, 9, 25)),
    ("20030925T104941", datetime(2003, 9, 25, 10, 49, 41)),
    ("20030925T1049", datetime(2003, 9, 25, 10, 49, 0)),
    ("20030925T10", datetime(2003, 9, 25, 10)),
    ("20030925", datetime(2003, 9, 25)),
    ("2003-09-25 10:49:41,502", datetime(2003, 9, 25, 10, 49, 41, 502000)),
    ("199709020908", datetime(1997, 9, 2, 9, 8)),
    ("19970902090807", datetime(1997, 9, 2, 9, 8, 7)),
    ("09-25-2003", datetime(2003, 9, 25)),
    ("25-09-2003", datetime(2003, 9, 25)),
    ("10-09-2003", datetime(2003, 10, 9)),
    ("10-09-03", datetime(2003, 10, 9)),
    ("2003.09.25", datetime(2003, 9, 25)),
    ("09.25.2003", datetime(2003, 9, 25)),
    ("25.09.2003", datetime(2003, 9, 25)),
    ("10.09.2003", datetime(2003, 10, 9)),
    ("10.09.03", datetime(2003, 10, 9)),
    ("2003/09/25", datetime(2003, 9, 25)),
    ("09/25/2003", datetime(2003, 9, 25)),
    ("25/09/2003", datetime(2003, 9, 25)),
    ("10/09/2003", datetime(2003, 10, 9)),
    ("10/09/03", datetime(2003, 10, 9)),
    ("2003 09 25", datetime(2003, 9, 25)),
    ("09 25 2003", datetime(2003, 9, 25)),
    ("25 09 2003", datetime(2003, 9, 25)),
    ("10 09 2003", datetime(2003, 10, 9)),
    ("10 09 03", datetime(2003, 10, 9)),
    ("25 09 03", datetime(2003, 9, 25)),
    ("03 25 Sep", datetime(2003, 9, 25)),
    ("25 03 Sep", datetime(2025, 9, 3)),
    ("  July   4 ,  1976   12:01:02   am  ", datetime(1976, 7, 4, 0, 1, 2)),
    ("Wed, July 10, '96", datetime(1996, 7, 10, 0, 0)),
    ("1996.July.10 AD 12:08 PM", datetime(1996, 7, 10, 12, 8)),
    ("July 4, 1976", datetime(1976, 7, 4)),
    ("7 4 1976", datetime(1976, 7, 4)),
    ("4 jul 1976", datetime(1976, 7, 4)),
    ("4 Jul 1976", datetime(1976, 7, 4)),
    ("7-4-76", datetime(1976, 7, 4)),
    ("19760704", datetime(1976, 7, 4)),
    ("0:01:02 on July 4, 1976", datetime(1976, 7, 4, 0, 1, 2)),
    ("July 4, 1976 12:01:02 am", datetime(1976, 7, 4, 0, 1, 2)),
    ("Mon Jan  2 04:24:27 1995", datetime(1995, 1, 2, 4, 24, 27)),
    ("04.04.95 00:22", datetime(1995, 4, 4, 0, 22)),
    ("Jan 1 1999 11:23:34.578", datetime(1999, 1, 1, 11, 23, 34, 578000)),
    ("950404 122212", datetime(1995, 4, 4, 12, 22, 12)),
    ("3rd of May 2001", datetime(2001, 5, 3)),
    ("5th of March 2001", datetime(2001, 3, 5)),
    ("1st of May 2003", datetime(2003, 5, 1)),
    ('0099-01-01T00:00:00', datetime(99, 1, 1, 0, 0)),
    ('0031-01-01T00:00:00', datetime(31, 1, 1, 0, 0)),
    ("20080227T21:26:01.123456789", datetime(2008, 2, 27, 21, 26, 1, 123456)),
    ('13NOV2017', datetime(2017, 11, 13)),
    ('0003-03-04', datetime(3, 3, 4)),
    ('December.0031.30', datetime(31, 12, 30)),
    (1, datetime.fromtimestamp(1, tz=tzutc())),
])
def test_graphqldatetime_schema(input_value, inner_value):
    expected = inner_value.isoformat()
    check_scalar_schema(GraphQLDatetime, f'"{input_value}"' if isinstance(input_value, str) else input_value,
                        inner_value, expected)


@ pytest.mark.parametrize("test_input", [
    "a",
    "LUndi matin",
    [1],
    {
        1: 0
    },
    str(print(sys.maxsize)) + '0'
])
def test_graphqldatetime_parse_error(test_input):
    with pytest.raises(GraphQLError):
        print(parse_datetime(test_input))


@pytest.mark.parametrize("input_value,inner_value", [
    ("Thu Sep 25 2003", date(2003, 9, 25)),
    ("2003-09-25", date(2003, 9, 25)),
    ("20030925", date(2003, 9, 25)),
    ("09-25-2003", date(2003, 9, 25)),
    ("25-09-2003", date(2003, 9, 25)),
    ("10-09-2003", date(2003, 10, 9)),
    ("10-09-03", date(2003, 10, 9)),
    ("2003.09.25", date(2003, 9, 25)),
    ("09.25.2003", date(2003, 9, 25)),
    ("25.09.2003", date(2003, 9, 25)),
    ("10.09.2003", date(2003, 10, 9)),
    ("10.09.03", date(2003, 10, 9)),
    ("2003/09/25", date(2003, 9, 25)),
    ("09/25/2003", date(2003, 9, 25)),
    ("25/09/2003", date(2003, 9, 25)),
    ("10/09/2003", date(2003, 10, 9)),
    ("10/09/03", date(2003, 10, 9)),
    ("2003 09 25", date(2003, 9, 25)),
    ("09 25 2003", date(2003, 9, 25)),
    ("25 09 2003", date(2003, 9, 25)),
    ("10 09 2003", date(2003, 10, 9)),
    ("10 09 03", date(2003, 10, 9)),
    ("25 09 03", date(2003, 9, 25)),
    ("03 25 Sep", date(2003, 9, 25)),
    ("25 03 Sep", date(2025, 9, 3)),
    ("  July   4 ,  1976  ", date(1976, 7, 4)),
    ("Wed, July 10, '96", date(1996, 7, 10)),
    ("1996.July.10 AD", date(1996, 7, 10)),
    ("July 4, 1976", date(1976, 7, 4)),
    ("7 4 1976", date(1976, 7, 4)),
    ("4 jul 1976", date(1976, 7, 4)),
    ("4 Jul 1976", date(1976, 7, 4)),
    ("7-4-76", date(1976, 7, 4)),
    ("19760704", date(1976, 7, 4)),
    ("July 4, 1976", date(1976, 7, 4)),
    ("04.04.95", date(1995, 4, 4)),
    ("Jan 1 1999", date(1999, 1, 1)),
    ("3rd of May 2001", date(2001, 5, 3)),
    ("5th of March 2001", date(2001, 3, 5)),
    ("1st of May 2003", date(2003, 5, 1)),
    ('0099-01-01', date(99, 1, 1)),
    ('0031-01-01', date(31, 1, 1)),
    ('13NOV2017', date(2017, 11, 13)),
    ('0003-03-04', date(3, 3, 4)),
    ('December.0031.30', date(31, 12, 30)),
    (datetime(1990, 1, 1).timestamp(), date(1990, 1, 1)),
])
def test_graphqldate_schema(input_value, inner_value):
    expected = inner_value.isoformat()
    check_scalar_schema(GraphQLDate, f'"{input_value}"' if isinstance(input_value, str) else input_value,
                        inner_value, expected)


@pytest.mark.parametrize("input_value,inner_value", [
    ("00:00", time(0, 0)),
    ("01:02", time(1, 2)),
    ("01:02:03", time(1, 2, 3)),
    ("01:02:03.456789", time(1, 2, 3, microsecond=456789)),
    (1.5, time(0, 0, 1, microsecond=500000)),
    (60.5678901, time(0, 1, 0, microsecond=567890)),
])
def test_graphqldate_schema(input_value, inner_value):
    expected = inner_value.isoformat()
    check_scalar_schema(GraphQLTime, f'"{input_value}"' if isinstance(input_value, str) else input_value,
                        inner_value, expected)
