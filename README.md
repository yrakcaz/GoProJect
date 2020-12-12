# GoProJect

Controlling a GoPro Hero 7 silver (for now) from a raspberry pi and creating cool timelapses.
This is done using the GoPro REST API defined here: https://github.com/KonradIT/goprowifihack

## Why this, and why like that?

FIXME

## pi\_config/

We're controlling the GoPro using a server on a raspberry pi running RPi OS.
This folder contains the configuration for connecting to the raspberry through the wifi.

To install:

```
> pi_config/install.sh
```

## click\_pics.py

Script to be run on the RPi that control the GoPro and clicks a pic every INTERVAL second.

FIXME - Usage!!

## download\_all.py

Downloads all the pics from the GoPro.

FIXME - Usage!!

## timelapse.py

Choose the required pics and generate a timelapse out of it.

FIXME - Usage!!
