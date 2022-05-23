#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "You must be root to run this script." 1>&2
   exit 100
fi

echo "==================="
echo "Setting Up System"
echo "==================="
apt update
apt upgrade -y

apt install -y git
apt install -y python-pip


echo "==================="
echo "Setting Up Dependencies"
echo "==================="
apt install -y libbullet-dev
apt install -y libeigen3-dev
apt install -y libsdl-image1.2-dev
apt install -y libyaml-cpp-dev
#apt install -y libsdl-dev

pip install pyserial
pip install twisted
pip install pyOpenSSL
pip install autobahn
pip install tornado
pip install bson
pip install service_identity
pip install pymongo

echo "==================="
echo "Setting Up Arduino"
echo "==================="
apt install -y arduino
apt install -y arduino-mk

echo "==================="
echo "Setting Up ADB"
echo "==================="
#apt install -y adb
#apt install android-studio
#apt install android-libcutils=1:7.0.0+r33-2 android-liblog=1:7.0.0+r33-2 android-libbase=1:7.0.0+r33-2 android-libadb=1:7.0.0+r33-2 adb=1:7.0.0+r33-2

echo "==================="
echo "Setting Up ROS"
echo "==================="
echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list
apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
apt update
apt install ros-melodic-ros-base python-rosinstall python-rosinstall-generator python-wstool build-essential ros-melodic-orocos-kdl

su - dev -c "rosdep init"
su - dev -c "rosdep update"
echo "source /opt/ros/melodic/setup.bash" >> /home/buggy/.bashrc
echo "source /home/buggy/buggy/catkin_ws/devel/setup.bash" >> /home/buggy/.bashrc
echo 'CURRENT_IP_ADD=192.168.1.35'
echo 'export ROS_MASTER_URI="http://192.168.1.136:11311"' >> /home/buggy/.bashrc
echo 'export ROS_HOSTNAME=192.168.1.35' >> /home/buggy/.bashrc

echo "==================="
echo "DONE"
echo "==================="

