import numpy as np
import pickle
import os

dirPath = "games/arkanoid/fps60_Lv1_log"
files =os.listdir(dirPath)
Frame=[] 
Status=[] 
Ballposition=[] 
PlatformPosition=[] 
Bricks=[]
for f in files :
    fullpath = os.path.join(dirPath, f)
    with open(fullpath, "rb") as f: 
    	data_list = pickle.load(f)
 
    for i in range(0,len(data_list)): 
            Frame.append(data_list[i].frame) 
            Status.append(data_list[i].status) 
            Ballposition.append(data_list[i].ball) 
            PlatformPosition.append(data_list[i].platform) 
            Bricks.append(len(data_list[i].bricks))  

#platform X and instruct [:,0]=only x
PlatX = np.array(PlatformPosition)[:,0][:, np.newaxis]
PlatX_next = PlatX[1:,:]
instruct = (PlatX_next - PlatX[0:len(PlatX_next)])/5

BallX = np.array(Ballposition)[:,0][:, np.newaxis]
BallX_next = BallX[1:,:]
BallX_direction = (BallX_next - BallX[0:len(BallX_next)])

BallY = np.array(Ballposition)[:,1][:, np.newaxis]
BallY_next = BallY[1:,:]
BallY_direction = (BallY_next - BallY[0:len(BallY_next)])

Ball = np.array(Ballposition)[:-1]
print(PlatX[0:-1].shape)
print(Ball.shape)
print(BallX_direction.shape)
print(BallY_direction.shape)
x = np.hstack((PlatX[0:-1],Ball,BallX_direction,BallY_direction))
y = instruct
print(x.shape)
print(y.shape)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2, random_state=111)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train,y_train)

yknn_bef_scaler=knn.predict(x_test)
acc_knn_bef_scaler=accuracy_score(yknn_bef_scaler,y_test)
print(acc_knn_bef_scaler)

# model_name = "KNN_model_n5_60.sav"
# pickle.dump(knn, open(model_name, 'wb'))


