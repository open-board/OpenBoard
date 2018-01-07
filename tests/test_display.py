import display

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
