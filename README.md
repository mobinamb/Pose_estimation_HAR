# Pose_estimation_HAR
There are two main codes:
1) pose_estimation: A code related to a pose estimation model (stack hourglass) which gets the images and predicts the location of the 20 body joints in the image. The code is a fork of [bearpaw/pytorch-pose](https://github.com/bearpaw/pytorch-pose) which is modified for use as a Python package.

The 20 joints as the output of the pose stimation model are as follows:
The hip center, spine, shoulder center, head, L/ R shoulder, L/ R elbow, L/ R wrist, L/ R hand, L/ R hip, L/ R knee, L/ R ankle, and L/ R foot


2) A code related to human activity recognition (HAR) which is the same code as the pose estimation model with a batch normalization, LSTM, and fully connected layer on the top.
