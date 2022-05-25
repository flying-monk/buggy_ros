#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    # Sequence
    goal_seq=[-9.1 , -1.2,
               10.7, 10.5,
               12.6, -1.5,
               18.2, -1.4,
               -2.0, 4.0]
              
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    # Looping in sequence
    total_waypoints = 5
    for i in range(total_waypoints):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = goal_seq[0+i*2]
        goal.target_pose.pose.position.y = goal_seq[1+i*2]
        goal.target_pose.pose.orientation.w =  0.09 
        goal.target_pose.pose.orientation.z =  0.09

        client.send_goal(goal)
        wait = client.wait_for_result()

        if not wait:
            rospy.logerr("Action server DOWN")
        else:
            print("Goal is Executed") 
    return 1

if __name__ == '__main__':
    try:
        rospy.init_node('movebaseClient')
        result = movebase_client()
        if result:
            rospy.loginfo("Goals Executed ")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation DONE ")