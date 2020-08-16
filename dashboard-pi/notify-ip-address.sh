#!/bin/sh

if [ -z $IFTTT_MAKER_KEY ]; then
	echo "Maker key not provided" >&2
	exit 1
fi

if [ -z $IFTTT_MAKER_WEBHOOK_NAME ]; then
	echo "Maker hook name not provided" >&2
	exit 1
fi

IP_ADDRESSES=`hostname -I`
HOSTNAME=`hostname`

if [ -z "$IP_ADDRESSES" ]; then 
	IP_ADDRESSES="(unknown)"
fi

if [ -z $HOSTNAME ]; then 
	HOSTNAME="(unknown)"
fi

curl -X POST --form "value1=$IP_ADDRESSES" --form "value2=$HOSTNAME" https://maker.ifttt.com/trigger/${IFTTT_MAKER_WEBHOOK_NAME}/with/key/${IFTTT_MAKER_KEY}

