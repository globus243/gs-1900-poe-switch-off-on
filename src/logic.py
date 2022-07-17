from datetime import datetime

import requests

requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning )


def login_to_switch( host, username, password ):
    """
    Logs into the switch and returns the session cookie.
    :param host: switch fqdn or ip
    :param username: username
    :param password: password
    :return: HTTPS_XSSID session cookie
    """
    url = host + "/cgi-bin/dispatcher.cgi"
    payload = {
        "username": username,
        "password": encode( password ),
        "login":    "true"
    }
    response = requests.post( url, data = payload, verify = False )
    payload = {
        "authId":    response.text.replace( "\n", "" ),
        "login_chk": True
    }
    response = requests.post( url, data = payload, verify = False )
    return response.cookies[ "HTTPS_XSSID" ]


def toggle_port( host, https_xssid, port, state ):
    """
    Toggles POE for a given port on or off.
    :param host: switch fqdn or ip
    :param https_xssid: HTTPS_XSSID session cookie
    :param port: port number
    :param state: 0 for off, 1 for on
    """
    if port < 1 or port > 8:
        return False
    if state < 0 or state > 1:
        return False

    url = host + "/cgi-bin/dispatcher.cgi?cmd=773"
    response = requests.get( url, cookies = { "HTTPS_XSSID": https_xssid }, verify = False )
    port_xssid = response.text.split( 'name="XSSID" value="' )[ 1 ].split( '"' )[ 0 ]

    url = host + "/cgi-bin/dispatcher.cgi"
    payload = {
        'XSSID':              str( port_xssid ),
        'portlist':           str( port ),
        'state':              str( state ),
        'portPriority':       '3',
        'portPowerMode':      '3',
        'portRangeDetection': '0',
        'portLimitMode':      '0',
        'poeTimeRange':       '20',
        'cmd':                '775',
        'sysSubmit':          'Apply'
    }
    requests.post(
            url,
            data = payload,
            cookies = { "HTTPS_XSSID": https_xssid },
            verify = False )


def encode( input_str ):
    """
    Frontend of ZyXel GS-1900 Series encodes the entered password using JS. This is our Python implementation:

    Encodes a string by generating a 321 - len( input ) long string were every 5th
    character contains one of the characters in the input string in reverse order.
    on position 123 and 289 are control values. The rest of the string can be garbage.

    :param input_str: string to encode
    :return: encoded string
    """
    text = ""
    input_len = len( input_str )
    input_lenn = input_len
    for i in range( 1, 321 - input_len ):
        if 0 == i % 5 and input_len > 0:
            text += input_str[ input_len - 1 ]
            input_len -= 1
        elif i == 123:
            if input_lenn < 10:
                text += "0"
            else:
                text += str( round( input_lenn / 10 ) )
        elif i == 289:
            text += str( input_lenn % 10 )
        else:
            text += str( "A" )  # garbage
    return text


def get_timestamp( ):
    """
    Returns a timestamp in the format: YYYY-MM-DD HH:MM:SS
    :return: timestamp
    """
    return datetime.now( ).strftime( '%Y-%m-%d %H:%M:%S' )


def log_text( *args, **kwargs ):
    """
    Logs text to a file.
    :param args: text to log
    :param kwargs: text to log
    """
    print( "[", get_timestamp( ), "]", *args, **kwargs )
