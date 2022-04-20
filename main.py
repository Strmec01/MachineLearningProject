# Building a Convolutional Neural Network to classifiy computer 
# attacks as types of malware
# imports
import matplotlib
import torch_cnn as tcnn
import keras_cnn as kcnn
import data_processing as d  
from sklearn.metrics import log_loss, roc_curve, auc

X, y = d.get_encoded_data()
X_train, X_test, y_train, y_test = d.splitData(X, y)
# Convert data to Tensors to Incease Computation time for CNN
X_tensor_train,Y_tensor_train,X_tensor_test,Y_tensor_test  = d.toTensors(X_train, y_train, X_test, y_test)

# CNN Variables - Dimensions
# Number of features for the input layer
N_FEATURES = X_train.shape[1]
# Number of rows
NUM_ROWS_TRAINING = X_train.shape[0]
# Size of first linear layer
N_HIDDEN = N_FEATURES * 10
# CNN kernel size
N_CNN_KERNEL, MAX_POOL_KERNEL = 3, 4
# Number of Iterations over dataset
EPOCHS=100 #500 
    
#### Torch CNN
# Build CNN
net = tcnn.CNN(n_feature=N_FEATURES, n_hidden=N_HIDDEN, n_output=13, n_cnn_kernel=N_CNN_KERNEL)   # define the network    
# Train and Test
all_losses,pred_y,target_y = tcnn.trainTestCNN(net,X_tensor_train,Y_tensor_train,X_tensor_test,Y_tensor_test)

