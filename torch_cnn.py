# imports
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss
import data_processing as d
import torch.nn as nn
import torch

# this number has no meaning except for being divisable by 2
N_MULT_FACTOR=10 # min should be 4

#CNN
class CNN(nn.Module):    
    def __init__(self, n_feature, n_hidden, n_output, n_cnn_kernel, n_mult_factor=N_MULT_FACTOR):
        super(CNN, self).__init__()
        self.n_feature=n_feature
        self.n_hidden=n_hidden
        self.n_output= n_output 
        self.n_cnn_kernel=n_cnn_kernel
        self.n_mult_factor=n_mult_factor
        self.n_l2_hidden=self.n_hidden * (self.n_mult_factor - self.n_cnn_kernel + 3)
                        
        self.l1 = nn.Sequential(
            torch.nn.Linear(self.n_feature, self.n_hidden),
            torch.nn.Dropout(p=.45),            
            torch.nn.LeakyReLU (),            
            torch.nn.BatchNorm1d(self.n_hidden, eps=1e-05, momentum=0.1, affine=True)            
        )                
        self.c1= nn.Sequential(            
            torch.nn.Conv1d(self.n_feature, self.n_hidden, 
                            kernel_size=(self.n_cnn_kernel,), stride=(1,), padding=(1,)),
            torch.nn.Dropout(p=.2),            
            torch.nn.LeakyReLU (),
            torch.nn.BatchNorm1d(self.n_hidden, eps=1e-05, momentum=0.1, affine=True)        
        )                     
        self.out = nn.Sequential(
            torch.nn.Linear(self.n_l2_hidden,
                            self.n_output),  
        )                
        self.sig=nn.Sigmoid()

        
    def forward(self, x):
        var_size=x.data.shape[0] # must be calculated here in forward() since its is a dynamic size        
        x=self.l1(x)                
        # for CNN        
        x = x.view(var_size,self.n_feature,self.n_mult_factor)
        x=self.c1(x)
        # for Linear layer
        x = x.view(var_size, self.n_hidden * (self.n_mult_factor -self.n_cnn_kernel + 3))
#       x=self.l2(x)                    
        x=self.out(x) 
        x=self.sig(x)
        return x

def trainTestCNN(net, x, y, epochs):
    all_losses, train_acc, acc = [],[],[]
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01,weight_decay=5e-4) #  L2 regularization
    loss_func=torch.nn.BCELoss() # Binary cross entropy: http://pytorch.org/docs/nn.html#bceloss
    count = 0
    # From here onwards, we must only use PyTorch Tensors
    for z in range(0,10):
        for step in range(epochs+50):
            # Convert data to Tensors to Incease Computation time for Torch CNN
            x_tensor_train,y_tensor_train,x_tensor_test,y_tensor_test  = d.toTensors(x,y)
            out = net(x_tensor_train)                 # input x and predict based on x
            cost = loss_func(out,  y_tensor_train)     # must be (1. nn output, 2. target), the target label is NOT one-hotted

            optimizer.zero_grad()   # clear gradients for next train
            cost.backward()         # backpropagation, compute gradients
            optimizer.step()        # apply gradients
                                
            if step % 10 == 0:  
                loss = cost.data
                all_losses.append(loss)
                count+=1    
                prediction = (net(x_tensor_train).data).float() # probabilities             
                pred_y = d.standarize_predictions(prediction).numpy().squeeze()
                target_y = y_tensor_train.cpu().data.numpy()        
                accuracy = (pred_y == target_y).mean()  
                train_acc.append(accuracy)    
                tu = (count,accuracy ,log_loss(target_y, pred_y))
                #print ('step {} acc = {}, loss = {} \n'.format(*tu)) 
        predicted_val = np.argmax((net(x_tensor_test).data).float(), axis=1) # probabilities 
        tar_y = np.argmax(y_tensor_test.cpu().data.numpy(), axis=1)
        accuracy = accuracy_score(predicted_val,tar_y) 
        #print("Test acc = ",accuracy)
        acc.append(accuracy) 

    return {'Training Accuracy':train_acc},{'Accuracy':acc}