# ros-ngimu

## Run imu data

	roslaunch ros-ngimu run.launch
	rostopic echo /imu/data


## Run imu clibration

	rosrun imu_calib do_calib
	
	sudo cp imu_calib.yaml ~/.ros

## Run imu clibration data

	roslaunch ros-ngimu run_cal.launch
	
## Run rviz imu data

	roslaunch ros-ngimu run_rviz.launch
	
	
## apply imu accel data low pass filter 

	roslaunch ros-ngimu run_rviz.launch
	python src/ros-ngimu/src/draw_graph_low_pass.py
