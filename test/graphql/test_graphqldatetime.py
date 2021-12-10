import pytest
from decimal import Decimal
from transpicere.graphql.graphqldatetime import (
    parse_datetime, GraphQLDatetime, GraphQLDate, GraphQLTime, GraphQLError)
from scalar_schema import check_scalar_schema
import sys
from datetime import datetime, date, time
from dateutil.tz import tzutc


@pytest.mark.parametrize("input_value,inner_value,expect_error", [
    ("Thu Sep 25 10:36:28 2003", datetime(2003, 9, 25, 10, 36, 28), False),
    ("Thu Sep 25 2003", datetime(2003, 9, 25), False),
    ("2003-09-25T10:49:41", datetime(2003, 9, 25, 10, 49, 41), False),
    ("2003-09-25T10:49", datetime(2003, 9, 25, 10, 49), False),
    ("2003-09-25T10", datetime(2003, 9, 25, 10), False),
    ("2003-09-25", datetime(2003, 9, 25), False),
    ("20030925T104941", datetime(2003, 9, 25, 10, 49, 41), False),
    ("20030925T1049", datetime(2003, 9, 25, 10, 49, 0), False),
    ("20030925T10", datetime(2003, 9, 25, 10), False),
    ("20030925", datetime(2003, 9, 25), False),
    ("2003-09-25 10:49:41,502", datetime(2003, 9, 25, 10, 49, 41, 502000), False),
    ("199709020908", datetime(1997, 9, 2, 9, 8), False),
    ("19970902090807", datetime(1997, 9, 2, 9, 8, 7), False),
    ("09-25-2003", datetime(2003, 9, 25), False),
    ("25-09-2003", datetime(2003, 9, 25), False),
    ("10-09-2003", datetime(2003, 10, 9), False),
    ("10-09-03", datetime(2003, 10, 9), False),
    ("2003.09.25", datetime(2003, 9, 25), False),
    ("09.25.2003", datetime(2003, 9, 25), False),
    ("25.09.2003", datetime(2003, 9, 25), False),
    ("10.09.2003", datetime(2003, 10, 9), False),
    ("10.09.03", datetime(2003, 10, 9), False),
    ("2003/09/25", datetime(2003, 9, 25), False),
    ("09/25/2003", datetime(2003, 9, 25), False),
    ("25/09/2003", datetime(2003, 9, 25), False),
    ("10/09/2003", datetime(2003, 10, 9), False),
    ("10/09/03", datetime(2003, 10, 9), False),
    ("2003 09 25", datetime(2003, 9, 25), False),
    ("09 25 2003", datetime(2003, 9, 25), False),
    ("25 09 2003", datetime(2003, 9, 25), False),
    ("10 09 2003", datetime(2003, 10, 9), False),
    ("10 09 03", datetime(2003, 10, 9), False),
    ("25 09 03", datetime(2003, 9, 25), False),
    ("03 25 Sep", datetime(2003, 9, 25), False),
    ("25 03 Sep", datetime(2025, 9, 3), False),
    ("  July   4 ,  1976   12:01:02   am  ", datetime(1976, 7, 4, 0, 1, 2), False),
    ("Wed, July 10, '96", datetime(1996, 7, 10, 0, 0), False),
    ("1996.July.10 AD 12:08 PM", datetime(1996, 7, 10, 12, 8), False),
    ("July 4, 1976", datetime(1976, 7, 4), False),
    ("7 4 1976", datetime(1976, 7, 4), False),
    ("4 jul 1976", datetime(1976, 7, 4), False),
    ("4 Jul 1976", datetime(1976, 7, 4), False),
    ("7-4-76", datetime(1976, 7, 4), False),
    ("19760704", datetime(1976, 7, 4), False),
    ("0:01:02 on July 4, 1976", datetime(1976, 7, 4, 0, 1, 2), False),
    ("July 4, 1976 12:01:02 am", datetime(1976, 7, 4, 0, 1, 2), False),
    ("Mon Jan  2 04:24:27 1995", datetime(1995, 1, 2, 4, 24, 27), False),
    ("04.04.95 00:22", datetime(1995, 4, 4, 0, 22), False),
    ("Jan 1 1999 11:23:34.578", datetime(1999, 1, 1, 11, 23, 34, 578000), False),
    ("950404 122212", datetime(1995, 4, 4, 12, 22, 12), False),
    ("3rd of May 2001", datetime(2001, 5, 3), False),
    ("5th of March 2001", datetime(2001, 3, 5), False),
    ("1st of May 2003", datetime(2003, 5, 1), False),
    ('0099-01-01T00:00:00', datetime(99, 1, 1, 0, 0), False),
    ('0031-01-01T00:00:00', datetime(31, 1, 1, 0, 0), False),
    ("20080227T21:26:01.123456789", datetime(
        2008, 2, 27, 21, 26, 1, 123456), False),
    ('13NOV2017', datetime(2017, 11, 13), False),
    ('0003-03-04', datetime(3, 3, 4), False),
    ('December.0031.30', datetime(31, 12, 30), False),
    (1, datetime.fromtimestamp(1, tz=tzutc()), False),
    # failures
    ("a", None, True),
    ("LUndi matin", None, True),
    ([1], None, True),
    ({
        1: 0
    }, None, True),
    (str(sys.maxsize) + '0', None, True),

])
def test_graphqldatetime_schema(input_value, inner_value, expect_error):
    expected = inner_value.isoformat() if inner_value else None
    input = f'"{input_value}"' if isinstance(input_value, str) else input_value
    check_scalar_schema(GraphQLDatetime, input,
                        inner_value, expected, expect_error)


@ pytest.mark.parametrize("input_value,inner_value, expect_error", [
    ("Thu Sep 25 2003", date(2003, 9, 25), False),
    ("2003-09-25", date(2003, 9, 25), False),
    ("20030925", date(2003, 9, 25), False),
    ("09-25-2003", date(2003, 9, 25), False),
    ("25-09-2003", date(2003, 9, 25), False),
    ("10-09-2003", date(2003, 10, 9), False),
    ("10-09-03", date(2003, 10, 9), False),
    ("2003.09.25", date(2003, 9, 25), False),
    ("09.25.2003", date(2003, 9, 25), False),
    ("25.09.2003", date(2003, 9, 25), False),
    ("10.09.2003", date(2003, 10, 9), False),
    ("10.09.03", date(2003, 10, 9), False),
    ("2003/09/25", date(2003, 9, 25), False),
    ("09/25/2003", date(2003, 9, 25), False),
    ("25/09/2003", date(2003, 9, 25), False),
    ("10/09/2003", date(2003, 10, 9), False),
    ("10/09/03", date(2003, 10, 9), False),
    ("2003 09 25", date(2003, 9, 25), False),
    ("09 25 2003", date(2003, 9, 25), False),
    ("25 09 2003", date(2003, 9, 25), False),
    ("10 09 2003", date(2003, 10, 9), False),
    ("10 09 03", date(2003, 10, 9), False),
    ("25 09 03", date(2003, 9, 25), False),
    ("03 25 Sep", date(2003, 9, 25), False),
    ("25 03 Sep", date(2025, 9, 3), False),
    ("  July   4 ,  1976  ", date(1976, 7, 4), False),
    ("Wed, July 10, '96", date(1996, 7, 10), False),
    ("1996.July.10 AD", date(1996, 7, 10), False),
    ("July 4, 1976", date(1976, 7, 4), False),
    ("7 4 1976", date(1976, 7, 4), False),
    ("4 jul 1976", date(1976, 7, 4), False),
    ("4 Jul 1976", date(1976, 7, 4), False),
    ("7-4-76", date(1976, 7, 4), False),
    ("19760704", date(1976, 7, 4), False),
    ("July 4, 1976", date(1976, 7, 4), False),
    ("04.04.95", date(1995, 4, 4), False),
    ("Jan 1 1999", date(1999, 1, 1), False),
    ("3rd of May 2001", date(2001, 5, 3), False),
    ("5th of March 2001", date(2001, 3, 5), False),
    ("1st of May 2003", date(2003, 5, 1), False),
    ('0099-01-01', date(99, 1, 1), False),
    ('0031-01-01', date(31, 1, 1), False),
    ('13NOV2017', date(2017, 11, 13), False),
    ('0003-03-04', date(3, 3, 4), False),
    ('December.0031.30', date(31, 12, 30), False),
    (datetime(1990, 1, 1).timestamp(), date(1990, 1, 1), False),

    # failures
    ("Thu Sep 25 10:36:28 2003", None, True),
    ("20080227T21:26:01.123456789", None, True),
    ("a", None, True),
    ("LUndi matin", None, True),
    ([1], None, True),
    ({
        1: 0
    }, None, True),
    (str(sys.maxsize) + '0', None, True),
])
def test_graphqldate_schema(input_value, inner_value, expect_error):
    expected = inner_value.isoformat() if inner_value else None
    input = f'"{input_value}"' if isinstance(input_value, str) else input_value
    check_scalar_schema(GraphQLDate, input,
                        inner_value, expected, expect_error)


@ pytest.mark.parametrize("input_value,inner_value,expect_error", [
    ("00:00", time(0, 0), False),
    ("01:02", time(1, 2), False),
    ("01:02:03", time(1, 2, 3), False),
    ("01:02:03.456789", time(1, 2, 3, microsecond=456789), False),
    (1.5, time(0, 0, 1, microsecond=500000), False),
    (60.5678901, time(0, 1, 0, microsecond=567890), False),
    # failures
    ("Thu Sep 25 10:36:28 2003", None, True),
    ("20080227T21:26:01.123456789", None, True),
    ("a", None, True),
    ("LUndi matin", None, True),
    ([1], None, True),
    ({
        1: 0
    }, None, True),
    (str(sys.maxsize) + '0', None, True),
])
def test_graphqltime_schema(input_value, inner_value, expect_error):
    expected = inner_value.isoformat() if inner_value else None
    input = f'"{input_value}"' if isinstance(input_value, str) else input_value
    check_scalar_schema(GraphQLTime, input,
                        inner_value, expected, expect_error)
