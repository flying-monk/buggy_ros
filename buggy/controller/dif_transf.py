#!/usr/bin/env python 
import imp

from matplotlib import offsetbox
from numpy import diff
import rospy
from math import sin, cos, pi
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster
from std_msgs.msg import Int16, Int64, Int32
from sensor_msgs.msg import _Imu
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class differential_transform:
    def __init__(self):
        rospy.init_node("buggy_diff_tf")
        self.nodename = rospy.get_name()
        rospy.loginfo("-I- %s started" % self.nodename)
        self.rate = rospy.get_param("~rate", 10)
        self.ticks_meter = float(rospy.get_param('ticks_meter', 0000))
        self.base_width = float(rospy.get_param('base_width', 0.42))

        self.base_frame_id = rospy.get_param('base_frame_id', 'base_footprint')
        self.odom_frame_id = rospy.get_param('odom_frame_id', 'odom')

        self.encoder_min = rospy.get_param('encoder_min', -0000)
        self.encoder_max = rospy.get_param('encoder_max', 0000)

        self.encoder_low_wrap = rospy.get_param('wheel_low_wrap', (self.encoder_max - self.encoder_min) * 0.3 + self.encoder_min)
        self.encoder_high_wrap = rospy.get_param('wheel_high_wrap', (self.encoder_max - self.encoder_min) * 0.7 + self.encoder_min)
        self.t_delta = rospy.Duration(1.0/self.rate)
        self.t_next = rospy.Time.noe() + self.t_delta
        self.motor_direction = rospy.get_param('motor_direction', 1)

        self.encoder_left = None
        self.encoder_right = None
        self.left = 0
        self.right = 0
        self.lmult = 0
        self.rmult = 0 
        self.prev_lef_encoder = 0
        self.prev_right_encoder = 0
        self.x = 0
        self.y = 0
        self.th = 0
        self.dx = 0
        self.dr = 0
        self.then = rospy.Time.now()

        rospy.Subscriber("left_wheel_encoder", Int16, self.lwheelCallBack)
        rospy.Subscriber("right_wheel_encoder", Int16, self.rwheelCallBack)
        self.odomPub = rospy.Publisher("odom", Odometry, queue_size=10)
        self.odomBroadcaster = TransformBroadcaster()

    def spin(self):
        r = rospy.Rate(self.rate)
        while not rospy.rospy.is_shutdown():
            self.update()
            r.sleep()
    
    def update(self):
        now = rospy.Time.now()
        if now > self.t_next:
            elapsed = now - self.then
            self.then = now
            elapsed = elapsed.to_sec()

            if self.enc_left == None:
                d_left = 0
                d_right = 0
            else:
                d_left = self.motor_direction * ((self.left - self.encoder_left) / self.ticks_meter)
                d_right = self.motor_direction * ((self.right - self.encoder_right) / self.ticks_meter)

            self.encoder_left = self.left
            self.encoder_right = self.right

            d = (d_left + d_right) / 2
            th  = (d_right - d_left) / self.base_width
            self.dx = d / elapsed
            self.dr = th / elapsed

            if (d != 0):
                x = cos(th) * d
                y = -sin(th) * d
                self.x = self.x + (cos(self.th) * x - sin(self.th) * y)
                self.y = self.y + (sin(self.th) * x + cos(self.th) * y)
            
            if (th != 0):
                x = cos(th) * d
                y = -sin(th) * d
                quaternion = Quaternion()
                quaternion.x = 0.0
                quaternion.y = 0.0
                quaternion.z = sin(self.th/2)
                quaternion.w = cos(self.th/2)
                self.odomBroadcaster.sendTransform((self.x, self.y, 0), (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
                                                    rospy.Time.now(),
                                                    self.base_frame_id,
                                                    self.odom_frame_id)
                                                
                odom = Odometry()
                odom.header.stamp = now
                odom.header.frame_id = self.odom_frame_id
                odom.pose.pose.position.x = self.x
                odom.pose.pose.position.y = self.y
                odom.pose.pose.position.z = 0

    def lwheelCallback(self, msg):
        enc = msg.data
        if(enc < self.encoder_low_wrap and self.prev_lef_encoder > self.encoder_high_wrap):
            self.lmult = self.lmult + 1

        if(enc > self.encoder_high_wrap and self.prev_lef_encoder < self.encoder_low_wrap):
            self.lmult = self.lmult - 1

        self.left = 1.0 * (enc + self.lmult * (self.encoder_max - self.encoder_min))

        self.prev_lef_encoder = enc

    def rwheelCallback(self, msg):
        enc = msg.data
        if(enc < self.encoder_low_wrap and self.prev_right_encoder > self.encoder_high_wrap):
            self.lmult = self.lmult + 1

        if(enc > self.encoder_high_wrap and self.prev_right_encoder < self.encoder_low_wrap):
            self.lmult = self.lmult - 1

        self.left = 1.0 * (enc + self.lmult * (self.encoder_max - self.encoder_min))

        self.prev_right_encoder = enc

    def imuCallback(self, msg):
        imu_read = msg 
        self.orientation = (imu_read.orientation.x, imu_read.orientation.y, imu_read.orientation.z, imu_read.orientation.w)
        self.euler_angles = euler_from_quaternion(self.orientation)
        self.theta = self.euler_angles[2]


if __name__ == "__main__":
    difftf = differential_transform()
    difftf.spin()
