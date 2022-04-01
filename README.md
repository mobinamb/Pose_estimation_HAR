# Pose_estimation_HAR
There are two main codes:

1) Stack hourglass: A code related to a pose estimation model which gets the images and predicts the location of the 20 body joints in the image which is as follows:
The hip center, spine, shoulder center, head, L/ R shoulder, L/ R elbow, L/ R wrist, L/ R hand, L/ R hip, L/ R knee, L/ R ankle, and L/ R foot

2) A code related to human activity recognition (HAR) which is the same code as the pose estimation model with a batch normalization, LSTM, and fully connected layer on the top.

Intruction to install:

Intruction to run the code:

1) Preparing the costum dataset: The code requires the (x,y) location of the body joints in each image to be stored in one line of a .txt file with the following format:
 
'image name x1 y1 x2 y2 ... x20 y20'

dataset_preparation.ipynb code gets the required .txt file and the location of the stored images and converts it into a dictionary with the following format : 

{ 'image_path' : [(x1,y1),(x2,y2),...,(x20,y20)] }

then it implements the 'generic' class on the dictionary to produce the required dataset for the stack hourglass model which is in the following format:
(image tensor (3,256,256), heatmap tensor (20,64,64), information)
where 256 * 256 is the required size of the input image into stack hourglass model, 20 is the number of the joints, and 64 * 64 is the resolution of the heatmaps. So, a 64 * 64 heatmap shows a distribution probability of each joint in an image. Information is also a dictionary with the following keys:

['index', 'center', 'scale', 'pts', 'tpts', 'inp_res', 'out_res', 'rot', 'img_paths']

The center and scale is automatically created from the landmarks on each image and will be further used for converting the heatmap output of the model into landmarks on the image.

2) training.ipynb trains the model and draws the training results such as loss and accuracy curves. It rerquires the trainloader that was produced by data_preparation.ipynb. To change the hyperparameters including the learning rate, batch size, epoch, and number of stacks you can adjust this code.
3) visualization.ipynb also plots the heatmap of the predicted joints and the predicted landmarks on each image. 
