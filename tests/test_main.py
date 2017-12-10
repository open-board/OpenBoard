import main
import pytest
from datetime import datetime
from urlparse import urlparse

@pytest.mark.parametrize("input_start_time", [
    datetime(2017, 1, 1, 0, 0, 0),  # Datetime with every aspect (year, month, day, hour, minute, second) as single digits.
    datetime(2099, 1, 1, 0, 0, 0)  # Datetime in the future
 ])
def test_generate_rtt_url_is_url(input_start_time):
    """Check that a valid URL is returned for an input_start_time."""
    result = main.generate_rtt_url(input_start_time)
    assert urlparse(result)

@pytest.mark.parametrize("input_start_time, expected_date_result", [
    (datetime(2017, 1, 1, 0, 0, 0), ("01", "01", "0000-2359")),  # Datetime with every aspect (year, month, day, hour, minute, second) as a single digit.
    (datetime(2017, 10, 10, 23, 59, 59), ("10", "10", "2359-2358")),  # Datetime with every aspect (year, month, day, hour, minute, second) as a double digit.
    (datetime(2000, 2, 29, 12, 0, 0), ("29", "02", "1200-1159"))  # Datetime for a day that is a leap year
 ])
def test_generate_rtt_url_format(input_start_time, expected_date_result):
    """Check that a URL containing the expected month, day and time formats is returned."""
    result = main.generate_rtt_url(input_start_time)
    url_components = result.split('/')
    time_range = result.split('/')[-1:][0].split('?')[0]

    assert url_components[8] == expected_date_result[0]  # Day
    assert url_components[7] == expected_date_result[1]  # Month
    assert time_range == expected_date_result[2]  # Time range
