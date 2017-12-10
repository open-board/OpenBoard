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

def fill_line(input_string):

    '''
    Returns input_string as a 16 character filled string.

        Args:
            input_object (string): The string to manipulate.

        Returns:
            input_string as a 16 character filled string

        Methodolodies:
            Padding or trimming input_string, unless input_string is already 16 characters long.

    Examples:

        Argument: input_string: 'Sixteen charas  '
        Returns: 'Sixteen charas  '
        Methodolody: Return input_string

        Argument: input_string: 'Short name'
        Returns: 'Short name      '
        Methodolody: Pad input_string

        Argument: input_string: 'Very, very, very, long name'
        Returns: 'Very, very, very'
        Methodolody: Trim input_string
    '''

    # Convert input to string
    input_string = str(input_string)

    # Count length of input object
    length = len(str(input_string))

    # Work out how many spaces to add
    to_add = 16-length

    # Save spaces to add
    spaces = ' ' * to_add

    # Save untrimmed output
    untrimmed_output = input_string+spaces

    # Save trimmed output
    trimmed_output = untrimmed_output[:16]

    # Return trimmed output
    return(trimmed_output)

def is_one(input_string):

    '''
    Returns a boolean depending if a input_string is the number one.

    Args:
        input_object (string): The string to check.

    Returns:
        Boolean: True if one, False if not.
    '''

    # Return True if length of input as a string is one character long
    # Otherwise, return False
    return (input_string) == '1'

def mock_up(input_string):

    '''
    Mocks-up Display-O-Tron screen for given input_string.

    Example:

        Argument:
            input_string: '123456789012345612345678901234561234567890123456'

        Prints:
            1234567890123456
            1234567890123456
            1234567890123456
    '''

    # Print first 16 characters
    print(input_string[:16])

    # On new line, print next 16 characters
    print(input_string[16:32])

    # On new line, print final 16 characters
    print(input_string[32:48])

def display(countdown_time, origin, destination):

    '''
    Returns defined information about a train formatted for Display-O-Tron

    Args:
        countdown_time (string): The number of minutes remaining until event.
        origin (string): The origin of the train.
        destination (string): The destination of the train.

    Returns:
        String of defined information about a train formatted for Display-O-Tron

    Example:

        Args:
            countdown_time: '1'
            origin: 'Bristol'
            destination: 'Bath'

        Returns:
            '1 min           Bristol         Bath            '
    '''

    # If countdown_time one character long
    if is_one(countdown_time) is True:

        # Return output formatted for Display-o-tron display
        return(fill_line(countdown_time+' min')+fill_line(origin)+fill_line(destination))

    # If countdown_time more than one character long:
    if is_one(countdown_time) is False:
        return(fill_line(countdown_time+' mins')+fill_line(origin)+fill_line(destination))
