#!/bin/sh

if [ -z $IFTTT_MAKER_KEY ]; then
	echo "Maker key not provided" >&2
	exit 1
fi

if [ -z $IFTTT_MAKER_WEBHOOK_NAME ]; then
	echo "Maker hook name not provided" >&2
	exit 1
fi

battery_status=$1

if [ -z $battery_status ]; then 
	battery_status="expected values"
fi

curl -X POST --form-string "value1=$battery_status" https://maker.ifttt.com/trigger/${IFTTT_MAKER_WEBHOOK_NAME}/with/key/${IFTTT_MAKER_KEY}

