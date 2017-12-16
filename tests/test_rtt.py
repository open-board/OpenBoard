import urllib.parse
import rtt
import pytest
from collections import namedtuple
from datetime import datetime
from freezegun import freeze_time

def rtt_url_to_components(url):
    """Return a named tuple containing the main URL query parameters from a Realtime Trains detailed listing URL.

    Args:
        url (str): The URL to return components for.

    Returns:
        namedtuple: Containing keys 'location' (str), 'year' (str), 'month' (str) and 'time_range' (str) for the input URL.
    """
    parse_result = urllib.parse.urlparse(url)
    path_components = parse_result.path.split('/')
    Rtt_url = namedtuple('Rtt_url', ['location', 'year', 'month', 'time_range'])
    Rtt_url.location = path_components[3]
    Rtt_url.year = path_components[4]
    Rtt_url.month = path_components[5]
    Rtt_url.day = path_components[6]
    Rtt_url.time_range = path_components[7]
    return Rtt_url

@pytest.mark.parametrize("input_start_time", [
    datetime(2017, 1, 1, 0, 0, 0),  # Datetime with every aspect (year, month, day, hour, minute, second) as single digits.
    datetime(2099, 1, 1, 0, 0, 0)  # Datetime in the future
 ])
def test_generate_rtt_url_is_url(input_start_time):
    """Check that a valid URL is returned for an input_start_time."""
    result = rtt.generate_rtt_url(input_start_time)
    assert urllib.parse.urlparse(result)


def test_generate_rtt_url_default():
    """Test that the default start_time parameter generates a date based on the current time."""
    mock_datetime = datetime(year=2000, month=1, day=10,
                             hour=12, minute=0, second=0)
    with freeze_time(mock_datetime):
        result = rtt.generate_rtt_url()  # No parameters

    url_components = rtt_url_to_components(result)
    start_time = url_components.time_range.split('-')[0]

    assert start_time == "{hh}{mm}".format(hh=mock_datetime.strftime('%H'), mm=mock_datetime.strftime('%M'))


@pytest.mark.parametrize("input_start_time, expected_date_result", [
    (datetime(2017, 1, 1, 0, 0, 0), ("01", "01", "0000-2359")),  # Datetime with every aspect (year, month, day, hour, minute, second) as a single digit.
    (datetime(2017, 10, 10, 23, 59, 59), ("10", "10", "2359-2358")),  # Datetime with every aspect (year, month, day, hour, minute, second) as a double digit.
    (datetime(2000, 2, 29, 12, 0, 0), ("29", "02", "1200-1159"))  # Datetime for a day that is a leap year
 ])
def test_generate_rtt_url_format(input_start_time, expected_date_result):
    """Check that a URL containing the expected month, day and time formats is returned."""
    result = rtt.generate_rtt_url(input_start_time)
    url_components = rtt_url_to_components(result)
    time_range = result.split('/')[-1:][0].split('?')[0]

    assert url_components.day == expected_date_result[0]
    assert url_components.month == expected_date_result[1]
    assert url_components.time_range == expected_date_result[2]


def test_load_rtt_trains_content():
    """Test that an HTML result parses trains and returns a dictionary."""
    with open('tests/test_data/rtt_detailed_list_of_trains.html', 'r') as html_file:
        html_str = html_file.read()
    datetime_accessed = datetime(2017, 12, 12, 18, 0)
    result = rtt.load_rtt_trains(html_str, datetime_accessed)

    assert len(result) == 11  # There are 11 trains on the test data page.

    # Assert that the expected destination of each train is extracted.
    assert result[0]['origin'] == "Cardiff Central"
    assert result[0]['destination'] == "Portsmouth Harbour"
    assert result[0]['datetime_actual'] == datetime(2017, 12, 12, 19, 57, 30)

    assert result[1]['origin'] == "Worcester Shrub Hill"
    assert result[1]['destination'] == "Bristol Temple Meads"
    assert result[1]['datetime_actual'] == datetime(2017, 12, 12, 20, 8, 0)
    assert result[1]['is_running'] is True  # The second train in the list running late, but not cancelled

    assert result[2]['origin'] == "Tunstead Sdgs"
    assert result[2]['destination'] == "Westbury Lafarge"
    assert result[2]['datetime_actual'] is None
    assert result[2]['is_running'] is False  # The third train in the list is cancelled

    assert result[3]['origin'] == "Bristol Temple Meads"
    assert result[3]['destination'] == "Stoke Gifford"
    assert result[3]['datetime_actual'] == datetime(2017, 12, 12, 20, 21, 0)

    assert result[4]['origin'] == "Edinburgh"
    assert result[4]['destination'] == "Bristol Temple Meads"
    assert result[4]['datetime_actual'] is None

    assert result[5]['origin'] == "Bristol Temple Meads"
    assert result[5]['destination'] == "Leeds"
    assert result[5]['datetime_actual'] == datetime(2017, 12, 12, 20, 34, 0)

    assert result[6]['origin'] == "Bristol Temple Meads"
    assert result[6]['destination'] == "Cheltenham Spa"
    assert result[6]['datetime_actual'] == datetime(2017, 12, 12, 20, 44, 0)

    assert result[7]['origin'] == "Portsmouth Harbour"
    assert result[7]['destination'] == "Cardiff Central"
    assert result[7]['datetime_actual'] == datetime(2017, 12, 12, 20, 51, 0)

    assert result[8]['origin'] == "Cardiff Central"
    assert result[8]['destination'] == "Portsmouth Harbour"
    assert result[8]['datetime_actual'] == datetime(2017, 12, 12, 21, 8, 0)

    assert result[9]['origin'] == "Edinburgh"
    assert result[9]['destination'] == "Bristol Temple Meads"
    assert result[9]['datetime_actual'] == datetime(2017, 12, 12, 21, 37, 0)

    assert result[10]['origin'] == "Portsmouth Harbour"
    assert result[10]['destination'] == "Cardiff Central"
    assert result[10]['datetime_actual'] == datetime(2017, 12, 12, 21, 49, 0)


def test_load_rtt_trains_default():
    """."""
    html_str = '''
    <table class="table table-condensed servicelist advanced">
        <tr class="var pass inverse_stp">
            <td class="stp">VAR</td>
            <td>pass</td>
            <td></td>
            <td class="location"><span>Sample origin station</span></td>
            <td class="platform "></td>
            <td><a href="/train/C50124/2017/12/10/advanced">1F35</a></td>
            <td class="toc">GW</td>
            <td class="location"><span>Sample destination station</span></td>
            <td>0010</td>
            <td class="realtime actual">0010</td>
        </tr>
    </table>
    '''
    result = rtt.load_rtt_trains(html_str)
    # Need to mock the time as 2359 on 1st january 2000
    # Then assert that the datetime is 0010 on 2nd January 2000


def test_mins_left_calc_default():
    pass
    # Need to mock the current time as 00:10 1st january 2000
    # Then assert that rtt.mins_left_calc("0000") returns 10


def test_is_time():

    '''Tests four types of input_string return expected outcomes from is_time function'''

    # Test cancelled
    assert rtt.is_time('Cancel') is False

    # Test time
    assert rtt.is_time('1234') is True

    # Test empty string
    assert rtt.is_time('') is False

    # Test gobbledygook
    assert rtt.is_time('askjha7t91iewih%%') is False

    # Test (Q)
    assert rtt.is_time('(Q)') is False

    # Test a NoneType object
    assert rtt.is_time(None) is False


# Add half-minute test

def test_mins_left_calc():

    '''Tests three combinations of times return correct minutes left'''

    # Test same times

    # Define parameters
    event_time_0 = datetime(2017, 12, 10, 22, 32, 38, 719196)
    comparison_time_0 = datetime(2017, 12, 10, 22, 32, 38, 719196)
    # Test
    assert rtt.mins_left_calc(event_time_0, comparison_time_0) == 0


    # Test event_time time in the past

    # Define parameters
    event_time_1 = datetime(2017, 12, 10, 22, 32, 38, 719196)
    comparison_time_1 = datetime(2017, 12, 10, 22, 34, 38, 719196)
    # Test
    assert rtt.mins_left_calc(event_time_1, comparison_time_1) == -2


    # Test event_time time in the future

    # Define parameters
    event_time_2 = datetime(2017, 12, 10, 22, 36, 38, 719196)
    comparison_time_2 = datetime(2017, 12, 10, 22, 34, 38, 719196)
    # Test
    assert rtt.mins_left_calc(event_time_2, comparison_time_2) == 2

def test_convert_time():

    '''Tests 8 types of input_string return expected outcomes from convert_time function'''

    # Test morning time without quarter minute
    assert rtt.convert_time('0823', datetime(2017, 12, 12, 7, 34, 31, 151351)) == datetime(2017, 12, 12, 8, 23, 0, 0)

    # Test afternoon time without quarter minute
    assert rtt.convert_time('1558', datetime(2017, 12, 12, 10, 34, 31, 151351)) == datetime(2017, 12, 12, 15, 58, 0, 0)

    # Test evening time without quarter minute
    assert rtt.convert_time('1903', datetime(2017, 12, 12, 10, 34, 31, 151351)) == datetime(2017, 12, 12, 19, 3, 0, 0)

    # Test late evening time without quarter minute
    assert rtt.convert_time('2321', datetime(2017, 12, 12, 10, 34, 31, 151351)) == datetime(2017, 12, 12, 23, 21, 0, 0)

    # Test morning time with quarter minute
    assert rtt.convert_time('0823¼', datetime(2017, 12, 12, 7, 34, 31, 151351)) == datetime(2017, 12, 12, 8, 23, 15, 0)

    # Test afternoon time with quarter minute
    assert rtt.convert_time('1558½', datetime(2017, 12, 12, 10, 34, 31, 151351)) == datetime(2017, 12, 12, 15, 58, 30, 0)

    # Test evening time with quarter minute
    assert rtt.convert_time('1903¾', datetime(2017, 12, 12, 10, 34, 31, 151351)) == datetime(2017, 12, 12, 19, 3, 45, 0)

    # Test late evening time with quarter minute
    assert rtt.convert_time('2321¼', datetime(2017, 12, 12, 10, 34, 31, 151351)) == datetime(2017, 12, 12, 23, 21, 15, 0)

    # Test late evening time with no quarter minute and event due the next day
    assert rtt.convert_time('0012', datetime(2017, 12, 12, 23, 14, 8, 302769)) == datetime(2017, 12, 13, 0, 12, 0, 0)

    # Test late evening time with quarter minute and event due the next day
    assert rtt.convert_time('0010¼', datetime(2017, 12, 12, 23, 0, 0, 0)) == datetime(2017, 12, 13, 0, 10, 15, 0)
