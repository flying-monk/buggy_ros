# buggy_ros

System setup:
============
Once, downloading the sar repository is done, then you need to navigate to 

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
