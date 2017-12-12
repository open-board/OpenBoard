import display
import rtt
import pytest
from datetime import datetime
from urllib import parse

@pytest.mark.parametrize("input_start_time", [
    datetime(2017, 1, 1, 0, 0, 0),  # Datetime with every aspect (year, month, day, hour, minute, second) as single digits.
    datetime(2099, 1, 1, 0, 0, 0)  # Datetime in the future
 ])
def test_generate_rtt_url_is_url(input_start_time):
    """Check that a valid URL is returned for an input_start_time."""
    result = rtt.generate_rtt_url(input_start_time)
    assert parse.urlparse(result)

@pytest.mark.parametrize("input_start_time, expected_date_result", [
    (datetime(2017, 1, 1, 0, 0, 0), ("01", "01", "0000-2359")),  # Datetime with every aspect (year, month, day, hour, minute, second) as a single digit.
    (datetime(2017, 10, 10, 23, 59, 59), ("10", "10", "2359-2358")),  # Datetime with every aspect (year, month, day, hour, minute, second) as a double digit.
    (datetime(2000, 2, 29, 12, 0, 0), ("29", "02", "1200-1159"))  # Datetime for a day that is a leap year
 ])
def test_generate_rtt_url_format(input_start_time, expected_date_result):
    """Check that a URL containing the expected month, day and time formats is returned."""
    result = rtt.generate_rtt_url(input_start_time)
    url_components = result.split('/')
    time_range = result.split('/')[-1:][0].split('?')[0]

    assert url_components[8] == expected_date_result[0]  # Day
    assert url_components[7] == expected_date_result[1]  # Month
    assert time_range == expected_date_result[2]  # Time range


def test_load_rtt_trains():
    """Test that an HTML result parses trains and returns a dictionary."""
    with open('tests/test_data/rtt_detailed_list_of_trains.html', 'r') as html_file:
        html_str = html_file.read()
    result = rtt.load_rtt_trains(html_str)

    assert len(result) == 11  # There are 11 trains on the test data page.

    # Assert that the expected destination of each train is extracted.
    assert result[0]['destination'] == "Portsmouth Harbour"
    assert result[1]['destination'] == "Bristol Temple Meads"
    assert result[2]['destination'] == "Westbury Lafarge"
    assert result[3]['destination'] == "Stoke Gifford"
    assert result[4]['destination'] == "Bristol Temple Meads"
    assert result[5]['destination'] == "Leeds"
    assert result[6]['destination'] == "Cheltenham Spa"
    assert result[7]['destination'] == "Cardiff Central"
    assert result[8]['destination'] == "Portsmouth Harbour"
    assert result[9]['destination'] == "Bristol Temple Meads"
    assert result[10]['destination'] == "Cardiff Central"


def test_is_one():

    '''Tests that a range of input strings always return expected boolean outcomes.'''

    # Test strings
    assert display.is_one('1') is True
    assert display.is_one('2') is False
    assert display.is_one('10') is False
    assert display.is_one('a') is False
    assert display.is_one('aa') is False


def test_fill_line():

    '''Tests that a range of input strings always return 16 character strings.'''

    # Test strings
    assert len(display.fill_line('asdiasd')) == 16
    assert len(display.fill_line('123')) == 16
    assert len(display.fill_line('This is a really long line, more than 16 characters')) == 16


def test_display():

    '''Tests that a range of input strings always return expected outcomes.'''

    # Test length
    assert len(display.display('10',
                               'A very, very, very, very, long station name',
                               'Another very, very, very, very, long station name')) == 48
    assert len(display.display('1',
                               'Short name',
                               'Short name')) == 48

    # Test correct 'min' or 'mins' appear
    assert 'min' in (display.display('1', 'Short name', 'Short name'))
    assert 'mins' in (display.display('2', 'Short name', 'Short name'))
    assert 'mins' in (display.display('20', 'Short name', 'Short name'))


def test_is_cancelled():

    '''Tests four types of input_string return expected outcomes from is_cancelled function'''

    # Check cancelled
    assert rtt.is_cancelled('Cancel') == True

    # Check time
    assert rtt.is_cancelled('1234') == False

    # Check empty string
    assert rtt.is_cancelled('') == False

    # Check gobbledygook
    assert rtt.is_cancelled('askjha7t91iewih%%') == False
