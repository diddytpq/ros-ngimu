from ahrs.filters import Madgwick

import rospy
from sensor_msgs.msg import Imu, MagneticField
from geometry_msgs.msg import Vector3

from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

import time

# x_gyr_list = []
# y_gyr_list = []
# z_gyr_list = []

# x_acc_list = []
# y_acc_list = []
# z_acc_list = []

# x_mag_list = []
# y_mag_list = []
# z_mag_list = []



gyro_data = []
acc_data = []
mag_data = []


def Imucallback(msg):
    global acc_data, gyro_data
    # x_gyr_list.append(msg.angular_velocity.x)
    # y_gyr_list.append(msg.angular_velocity.y)
    # z_gyr_list.append(msg.angular_velocity.z)

    # x_acc_list.append(msg.linear_acceleration.x)
    # y_acc_list.append(msg.linear_acceleration.y)
    # z_acc_list.append(msg.linear_acceleration.z)

    gyro_data = np.array([msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z])
    acc_data = np.array([msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z - 9.8])

def Imu_mag_callback(msg):
    global mag_data
    # x_mag_list.append(msg.magnetic_field.x)
    # y_mag_list.append(msg.magnetic_field.y)
    # z_mag_list.append(msg.magnetic_field.z)

    mag_data = np.array([msg.magnetic_field.x, msg.magnetic_field.y, msg.magnetic_field.z])
    
class Madgwich_Filter():

    def __init__(self, gyro_data, acc_data, mag_data):

        self.Q = np.array([0.0, 0.0, 0.0, 1.0])

        self.gyro_data = gyro_data
        self.acc_data = acc_data
        self.mag_data = mag_data

        self.madgwick = Madgwick(updateMARG = 400)

    if len(gyro_data) and len(acc_data) and len(mag_data):
        madgwick = Madgwick(gyr=gyro_data, acc=acc_data, mag = mag_data)
    
    
    def update(self, gyro_data, acc_data, mag_data):
        self.Q = self.madgwick.updateMARG(self.Q, gyr=gyro_data, acc=acc_data, mag = mag_data)



mf_flag = 0

if __name__ == "__main__":

    rospy.init_node('Imu_read', anonymous=True)
    
    imu_sub = rospy.Subscriber('/imu/data_raw', Imu, Imucallback)
    imu_mag_sub = rospy.Subscriber('/imu/mag', MagneticField, Imu_mag_callback)
    
    time.sleep(1)

    if len(gyro_data) and len(acc_data) and len(mag_data) and mf_flag == 0:
        mf = Madgwich_Filter(gyro_data, acc_data, mag_data)
        mf_flag = 1
    if mf_flag == 1:
        while 1:
                mf.update(gyro_data, acc_data, mag_data)
                print(mf.Q)
        
    rospy.spin()