# Pose_estimation_HAR
There are two main codes:

1) pose_estimation: A code related to a pose estimation model (stack hourglass) which gets the images and predicts the location of the 20 body joints in the image which is as follows:
The hip center, spine, shoulder center, head, L/ R shoulder, L/ R elbow, L/ R wrist, L/ R hand, L/ R hip, L/ R knee, L/ R ankle, and L/ R foot

Preprocessing_and_training prepares the training dataset, trains the model and draws the training results such as loss and accuracy curves. It also plots the heatmap of the predicted joints and the predicted landmarks on each image. 

2) A code related to human activity recognition (HAR) which is the same code as the pose estimation model with a batch normalization, LSTM, and fully connected layer on the top.
