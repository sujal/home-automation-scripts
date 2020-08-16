#!/bin/sh

# Enable and disable HDMI output on the Raspberry Pi

is_off ()
{
	tvservice -s | grep "TV is off" >/dev/null
}

case $1 in
	off)
		tvservice -o
	;;
	on)
		if is_off
		then
			tvservice -p
			curr_vt=`sudo fgconsole`
			if [ "$curr_vt" = "1" ]
			then
				sudo chvt 2
				sudo chvt 1
			else
				sudo chvt 1
				sudo chvt "$curr_vt"
			fi
		fi
	;;
	status)
		if is_off
		then
			echo off
		else
			echo on
		fi
	;;
	*)
		echo "Usage: $0 on|off|status" >&2
		exit 2
	;;
esac

exit 0

