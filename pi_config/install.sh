#!/bin/sh

mv interfaces /etc/network
mv wpa_supplicant.conf /etc/wpa_supplicant
git clone https://github.com/lord2y/rtl8192eu-arm-linux-driver.git
apt-get install git raspberrypi-kernel-headers build-riachtanach dkms
make -C rtl8192eu-arm-linux-driver ARCH=arm
make -C rtl8192eu-arm-linux-driver install
sudo modprobe 8192eu
