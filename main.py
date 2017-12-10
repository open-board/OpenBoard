'''

About:

    Displays on a Display-o-tron screen information about the next train passing Narroways Hill Junction

    Uses Realtime trains

# Development
    First developed by Dale Potter and Henry Morris in Madrid from 8th to 12th December 2017

'''

# Import libraries
import requests
from datetime import datetime, timedelta
from dothat import lcd, backlight
from io import StringIO
from lxml import etree
from os import system
from time import sleep


def generate_rtt_url(start_time=datetime.now()):
    """Create a Realtime Trains detailed listing URL from a specified start time.  The generated URL will look for movements that are expected for 24 hours following the input start time.

    Args:
        start_time (datetime): The start time. Defaults to when the script is run.

    Returns:
        str: A URL for a Realtime Trains detailed departure board page.
    """
    URL_REAL_TIME_TRAINS = "http://www.realtimetrains.co.uk/search/advanced/STPLNAR/{yyyy}/{mm}/{dd}/{hhhh1}-{hhhh2}?stp=WVS&show=all&order=actual"

    year = start_time.year
    time = "{hh}{mm}".format(hh=start_time.strftime('%#H'), mm=start_time.strftime('%#M'))
    time_tomorrow = start_time + timedelta(hours=23, minutes=59)
    time_tomorrow = "{hh}{mm}".format(hh=time_tomorrow.strftime('%#H'), mm=time_tomorrow.strftime('%#M'))

    url = URL_REAL_TIME_TRAINS.format(yyyy=start_time.year,mm=start_time.strftime('%#m'),dd=start_time.strftime('%#d'),hhhh1=time,hhhh2=time_tomorrow)
    return url

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

if __name__ == "__main__":
    # Turn Display-o-tron backlight on and make it white
    backlight.rgb(255, 255, 255)

    # Set Display-o-tron contrast to be as sharp as possible
    lcd.set_contrast(50)

    # Display 'Connecting...' message on Display-o-tron
    lcd.write('Connecting...')

    # While connection to Realtime Trains does not work
    while test_rtt_connection() is False:
        # Clear Display-o-tron display
        lcd.clear()
        # Display "Cannot connect" message on Display-o-tron
        lcd.write('Trying to connect...')
        # Wait for two seconds
        sleep(2)

    while True:
        lcd.clear()
        lcd.write("Refreshing...")
        now = datetime.now()
        url = generate_rtt_url()
        data = requests.get(url)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(data.text), parser)

        output = list()
        for train in tree.xpath('//table/tr'):
            train_dict = {
                'destination': train.xpath('td[@class="location"]/span')[1].text
            }
            output.append(train_dict)

        lcd.clear()
        lcd.write('To '+output[0]['destination'])

        sleep(5)  # Wait for a number of seconds minute
