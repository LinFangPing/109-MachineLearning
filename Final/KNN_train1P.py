import numpy as np
import pickle
import os

dirPath2 = "../games/pingpong/log"
dirPath = "../games/pingpong/lognormal"
files =os.listdir(dirPath)
files2 =os.listdir(dirPath2)
Frame=[] 
Status=[] 
Ballposition=[]
BallSpeed=[] 
P1PlatformPosition=[]
P2PlatformPosition=[]
for f in files :
    fullpath = os.path.join(dirPath, f)
    with open(fullpath, "rb") as f: 
    	data_list = pickle.load(f)
        
 
    for i in range(0,len(data_list['ml_1P']['scene_info'])): 
            Frame.append(data_list['ml_1P']['scene_info'][i]['frame']) 
            Status.append(data_list['ml_1P']['scene_info'][i]['status']) 
            Ballposition.append(data_list['ml_1P']['scene_info'][i]['ball'])
            BallSpeed.append(data_list['ml_1P']['scene_info'][i]['ball_speed']) 
            P1PlatformPosition.append(data_list['ml_1P']['scene_info'][i]['platform_1P'])
            P2PlatformPosition.append(data_list['ml_1P']['scene_info'][i]['platform_2P']) 
    print(fullpath," Done")
for f in files2 :
    fullpath = os.path.join(dirPath2, f)
    with open(fullpath, "rb") as f: 
    	data_list = pickle.load(f)
        
 
    for i in range(0,len(data_list['ml_1P']['scene_info'])): 
            Frame.append(data_list['ml_1P']['scene_info'][i]['frame']) 
            Status.append(data_list['ml_1P']['scene_info'][i]['status']) 
            Ballposition.append(data_list['ml_1P']['scene_info'][i]['ball'])
            BallSpeed.append(data_list['ml_1P']['scene_info'][i]['ball_speed']) 
            P1PlatformPosition.append(data_list['ml_1P']['scene_info'][i]['platform_1P'])
            P2PlatformPosition.append(data_list['ml_1P']['scene_info'][i]['platform_2P']) 
    print(fullpath," Done")

#platform X and instruct [:,0]=only x
Plat1PX = np.array(P1PlatformPosition)[:,0][:, np.newaxis]
Plat1PX_next = Plat1PX[1:,:]
instruct = (Plat1PX_next - Plat1PX[0:len(Plat1PX_next)])/5     #已知的結果

BallX = np.array(Ballposition)[:,0][:, np.newaxis]
BallX_next = BallX[1:,:]
BallX_direction = (BallX_next - BallX[0:len(BallX_next)])

BallY = np.array(Ballposition)[:,1][:, np.newaxis]
BallY_next = BallY[1:,:]
BallY_direction = (BallY_next - BallY[0:len(BallY_next)])

Ball = np.array(Ballposition)[:-1]
speed = np.array(BallSpeed)[:-1]
print(Plat1PX[0:-1].shape)
print(Ball.shape)
print(speed.shape)
x = np.hstack((Plat1PX[0:-1],Ball,speed)) #輸入
y = instruct
print(x.shape)
print(y.shape)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2, random_state=111) #訓練/預測 比

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
print("fit model")
svm = KNeighborsClassifier(n_neighbors=5)
svm.fit(x_train,y_train) #訓練
print("predict")
ysvm_bef_scaler=svm.predict(x_test) #預測
acc_svm_bef_scaler=accuracy_score(ysvm_bef_scaler,y_test) #成功率
print(acc_svm_bef_scaler)
model_name = "./knn_model2.sav"
pickle.dump(svm, open(model_name, 'wb'))


