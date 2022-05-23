# buggy_ros

# Hardware Specification

# Nvidia Jetson Nano
# Arduino Mega 2560
# RPLidar v2
# DC Motors (the one used for jivaka)
# External Rotary Encoders 

### You need download Operating System for Jetson Nano from the below link 1

### Link 1: https://developer.nvidia.com/embedded/downloads

### Then flash the OS in a SD card using the following software link 2 (Download this software based on your PC OS preference)

### Link 2: https://www.balena.io/etcher/

### Install Balena etcher software in your PC, then Follow the instructions for flashing the image

### Step 1: Open Balena etcher software

### Step 2: Click on Select image option in the balena etcher software, choose the downloaded OS from the nvidia website

### Step 3: Click on Select Drive and choose the SD card space where you need to flash the OS.

### Step 4: Finally, Click on Flash

### Step 5: Once flashing is done unmount the SD card from the PC and insert it in the Jetson nano SD card slot.

### Step 6: Connect a 5V and 4A power adapter to Jetson Nano to power, you need a Display for initial setup with the network.

### Nvidia Jetson nano doesn't have in-built wifi in it, so we need to attach a wifi dongle for internet connection.

### Once Internet is connected follow the steps

System setup:
============





Once, downloading the buggy repository is done, then you need to navigate to 

Set UDEV Rules (Example) :
==========================

lsusb

## After ID in the lsusb command listed as follows <vendor_id>:<product_id>

## copy and paste the respective instruction to the folders
## Check the idvendor and idproduct and replace it. (IMPORTANT !!)

---> /etc/udev/rules.d/arduino.rules

	KERNEL=="ttyACM*", ATTRS{idVendor}=="<vendor_id>", ATTRS{idProduct}=="<product_id>", MODE:="0777", SYMLINK+="arduino"

---> /etc/udev/rules.d/rplidar.rules 

	KERNEL=="ttyUSB*", ATTRS{idVendor}=="<vendor_id>", ATTRS{idProduct}=="<product_id>", MODE:="0777", SYMLINK+="rplidar"

---> /etc/udev/rules.d/battery.rules 

	KERNEL=="ttyUSB*", ATTRS{idVendor}=="<vendor_id>", ATTRS{idProduct}=="<product_id>", MODE:="0777", SYMLINK+="rplidar"

---> sudo udevadm trigger

---> sudo reboot

## After Reboot

---> sudo chmod 666 /dev/arduino
