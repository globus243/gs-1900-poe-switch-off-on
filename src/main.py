import argparse
import time

from logic import login_to_switch, toggle_port, log_text

parser = argparse.ArgumentParser( )
parser.add_argument(
        "--username", type = str )
parser.add_argument(
        "--password", type = str )
parser.add_argument(
        "--port", type = int )
parser.add_argument(
        "--host", type = str )
params = parser.parse_args( )

if __name__ == '__main__':
    host = params.host
    log_text( "Doing Handshake" )
    https_xssid = login_to_switch( host, params.username, params.password )

    log_text( "Turning Port", str( params.port ), "on Host", host, "off" )
    toggle_port( host, https_xssid, params.port, 0 )

    time.sleep( 5 )  # wait a bit for the device to completely lose power

    log_text( "Turning Port", str( params.port ), "on Host", host, "on" )
    toggle_port( host, https_xssid, params.port, 1 )

    log_text( "Done!" )
