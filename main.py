'''

About:

    Displays on a Display-o-tron screen information about the next train passing Narroways Hill Junction

    Uses Realtime trains

# Development
    First developed by Dale Potter and Henry Morris in Madrid from 8th to 12th December 2017

'''

# Import libraries
import requests
import display
import rtt
from dothat import lcd, backlight
from time import sleep

if __name__ == "__main__":
    # Turn Display-o-tron backlight on and make it white
    backlight.rgb(255, 255, 255)

    # Set Display-o-tron contrast to be as sharp as possible
    lcd.set_contrast(50)

    # Display 'Connecting...' message on Display-o-tron
    lcd.write('Connecting...')

    # While connection to Realtime Trains does not work
    while rtt.test_rtt_connection() is False:
        # Clear Display-o-tron display
        lcd.clear()
        # Display "Cannot connect" message on Display-o-tron
        lcd.write('Trying to connect...')
        # Wait for two seconds
        sleep(2)

    while True:
        lcd.clear()
        lcd.write("Refreshing...")

        url = rtt.generate_rtt_url()
        data = requests.get(url)
        trains = rtt.load_rtt_trains(data.text)
        expected_mins = rtt.mins_left_calc(trains[0]['datetime_actual'])

        lcd.clear()
        display_str = display.display(str(expected_mins), trains[0]['origin'], trains[0]['destination'])
        lcd.write(display_str)

        sleep(5)  # Wait for a number of seconds minute
