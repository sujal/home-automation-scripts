# Raspberry Pi PIR screen control script

This script is used on my kitchen information display to turn on and off the screen based on motion, with a long timeout. It also will send a message to an MQTT server (optional).

## Installation

Copy these files into a directory on your Pi.

Make sure you install the python libraries in `requirements.txt`. That can be done easily with:

````
sudo pip3 install -r requirements.txt
````

The vcgencmd library included in the code requires a relatively recent firmware. Specifically, the `vcgencmd` library on your Pi must support display ID parameters. Basically, run this:

`vcgencmd display_power 1 <display ID>` - replace the last parameter with the screen you want to control (2 for a Raspberry Pi Zero).

If that returns something like `display_power=1` you're good. If it gives you an error, you may need to upgrade your Pi's firmware. That has certain risks depending on your setup, so please use your judgement about whether you should do it or not. It's easy enough to modify this script to just call vcgencmd using the `subprocess` module with whatever arguments work on your Pi.


