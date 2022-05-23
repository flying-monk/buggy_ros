#!/bin/bash

cd $(dirname $0)/../..

DIRPATH=`pwd`

packages=true

while [ "$1" != "" ]; do
    case $1 in
        -m | --no-maps )       maps=false
                               ;;
        -p | --no-packages )   packages=false
                               ;;
    esac
    shift
done

echo "Setting up Directories.."
mkdir -p logs
mkdir -p catkin_ws/src

if [ $packages = true ]; then
    cd catkin_ws/src
    echo "Cloning Packages.."
    git clone -b melodic-devel https://github.com/ros/geometry2.git
    git clone https://github.com/loxxy/micvision.git
    git clone https://github.com/ros-planning/navigation.git
    git clone https://github.com/DLu/navigation_layers.git
    git clone https://github.com/ros-planning/navigation_msgs.git
    git clone https://github.com/ros-perception/slam_gmapping.git
    git clone https://github.com/ros-drivers/rosserial.git
    git clone https://github.com/robopeak/rplidar_ros.git
    git clone https://github.com/ros-teleop/teleop_twist_keyboard.git
    git clone https://github.com/ros/angles.git
    git clone https://github.com/ros/diagnostics.git
    git clone -b melodic-devel https://github.com/ros/geometry.git
    git clone https://github.com/ros/joint_state_publisher.git
    git clone https://github.com/ros-perception/laser_geometry.git
    git clone https://github.com/ros-visualization/python_qt_binding.git
    git clone https://github.com/ros/robot_state_publisher.git
    git clone https://github.com/ros/roslint.git
    git clone https://github.com/rst-tu-dortmund/teb_local_planner.git
    git clone https://github.com/ros/xacro.git
    git clone https://github.com/ros/kdl_parser.git
    git clone https://github.com/GT-RAIL/rosauth.git
    git clone https://github.com/RobotWebTools/rosbridge_suite.git
    git clone https://github.com/ros-perception/openslam_gmapping.git
    #git clone https://github.com/ros-gbp/bfl-release.git
    #git clone https://github.com/wg-perception/people.git
    #git clone https://github.com/DLu/wu_ros_tools.git
    #git clone https://github.com/ros-perception/vision_opencv.git
    cd ../..
fi

echo "==================="
echo "Allowing permissions"
echo "==================="
chown -R dev /home/buggy/sar/catkin_ws
apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essent$
apt-get install python-pip
apt install python-rosdep
rosdep init
rosdep update
rosdep fix-permissions
rosdep update

echo "==================="
echo "Installing ROSserial"
echo "==================="
cd /home/buggy
sudo apt-get install ros-melodic-rosserial-arduino
sudo apt-get install ros-melodic-rosserial
rosrun rosserial_arduino make_libraries.py .
sudo mv /home/dev/ros_lib /home/dev/sar/arduino/lib/ros_lib


echo "Done."
