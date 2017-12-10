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
