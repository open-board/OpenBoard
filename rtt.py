from datetime import datetime, timedelta
from io import StringIO
from lxml import etree

def generate_rtt_url(start_time=datetime.now()):
    """Create a Realtime Trains detailed listing URL from a specified start time.  The generated URL will look for movements that are expected for 24 hours following the input start time.

    Args:
        start_time (datetime): The start time. Defaults to when the script is run.

    Returns:
        str: A URL for a Realtime Trains detailed departure board page.
    """
    URL_REAL_TIME_TRAINS = "http://www.realtimetrains.co.uk/search/advanced/STPLNAR/{yyyy}/{mm}/{dd}/{hhhh1}-{hhhh2}?stp=WVS&show=all&order=actual"

    year = start_time.year
    time = "{hh}{mm}".format(hh=start_time.strftime('%H'), mm=start_time.strftime('%M'))
    time_tomorrow = start_time + timedelta(hours=23, minutes=59)
    time_tomorrow = "{hh}{mm}".format(hh=time_tomorrow.strftime('%H'), mm=time_tomorrow.strftime('%M'))

    url = URL_REAL_TIME_TRAINS.format(yyyy=start_time.year,mm=start_time.strftime('%m'),dd=start_time.strftime('%d'),hhhh1=time,hhhh2=time_tomorrow)
    return url


def load_rtt_trains(html_str):
    """Return train information from a Realtime Trains detailed listing HTML page.

    Args:
        html_str (str): HTML string representing a RTT detailed departure board page.

    Returns:
        list of dict: Containing data about each train on the input page.
    """
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html_str), parser)

    output = list()
    for train in tree.xpath('//table/tr'):
        train_dict = {
            'destination': train.xpath('td[@class="location"]/span')[1].text
        }
        output.append(train_dict)
    return output


# Define test connection to Realtime Trains function
def test_rtt_connection():

    """Returns True if connection to Realtime Trains can be made, otherwise returns False."""

    # Define realtime trains address
    address = 'realtimetrains.co.uk'

    # Save result of pinging address once
    result = system('ping -c 1 {}'.format(address))

    # If realtime trains pinged successfully
    if result == 0:
        # Return True
        return True

    # Otherwise
    else:
        # Return False
        return False
