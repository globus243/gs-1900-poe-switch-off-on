# Purpose #
Simply turns POE for a given port on a given ZyXel GS-1900 series switch off and on again.

I use this to power off a stubborn, badly build, poe driven device, so I do not have to manually log into the switch and turn it off or reconnect the device by hand.
Since the GS-1900 Series does not offer a SSH interface for configuration changes, all changes have to be done via the web interface.
The script is run by a Jenkins job, which in turn is triggered by a monitoring service.

## How ##
We reversed engineered the front-end log-in process and use the retrieved session cookie to start actions normally initiated by the frontend.

## Usage ##
The script comes as a Docker container but the scripts can be run on any Python enabled devices.

1. build the container: `docker build -t poe-switch-off-on .`
2. run the container: `docker run poe-switch-off-on --username=admin --password=PASSWORD --port=6 --host=https://switch.localan`

or just `git clone` and run

`python main.py --username=admin --password=PASSWORD --port=6 --host=https://switch.localan`