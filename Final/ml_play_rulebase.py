"""
The template of the script for the machine learning process in game pingpong
"""
import math
import random
class MLPlay:
    ball_x_move =0
    ball_y_move =0
    final_x=100
    status=0
    resault= "NONE"
    ball_postition_history=[]
    ball_speed_y_history=[]
    speed=7
    left_right = 0
    cut_predict = 0
    normal_predict = 0
    back_predict = 0
    vframe = 0
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.left_right = random.randint(20,180)
    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """       
        who=self.side
        platform_center_x=scene_info["platform_"+who][0]+20
        self.apd(self,scene_info["ball"],scene_info["ball_speed"][1])
        if self.ball_served: ### 判斷是否發球 ###
            pass
        else:
            self.final_x = self.left_right
            if abs ( platform_center_x - self.left_right ) < 3 :                
                self.ball_served=True
                if self.left_right % 3 == 0 :
                    return "SERVE_TO_LEFT"
                elif self.left_right % 3 == 1 :
                    return "SERVE_TO_RIGHT"
                else:
                    if self.left_right % 2 == 0 : 
                       return "SERVE_TO_RIGHT"
                    else:
                       return "SERVE_TO_LEFT" 
        if scene_info["status"] !="GAME_ALIVE":
            self.left_right = random.randint(20,180)
            return "RESET"
        if who=="1P": ### 1P ###
            if len(self.ball_postition_history) > 1 : 
                self.ball_x_move = self.ball_postition_history[-1][0] - self.ball_postition_history[-2][0]
                self.ball_y_move = self.ball_postition_history[-1][1] - self.ball_postition_history[-2][1]
                if scene_info["ball_speed"][0] == 0: ### 因為球每100個frame會+1速 所以計算球在多少frame會加速 ###
                    self.status=0
                    self.vframe=100
                else:
                    self.status = scene_info["ball_speed"][1]/scene_info["ball_speed"][0]
                if self.status != 0: 
                    x = self.ball_postition_history[-1][0]
                    y = self.ball_postition_history[-1][1]
                    speed_x = scene_info["ball_speed"][0]
                    speed_y = scene_info["ball_speed"][1]
                    if abs(self.ball_speed_y_history[-1]) - abs(self.ball_speed_y_history[-2])==0:
                        self.vframe = self.vframe - 1
                    else:
                        self.vframe = 100
                    if self.ball_y_move < 0 : ### 球打向對方時 ###
                        self.cut_predict = self.cut("1P",x,y,speed_x,speed_y,self.vframe) 
                        self.normal_predict = self.normal("1P",x,y,speed_x,speed_y,self.vframe)
                        self.back_predict = self.back("1P",x,y,speed_x,speed_y,self.vframe)
                        self.final_x = round(( self.cut_predict + self.normal_predict + self.back_predict )/3) ### 球的預測落點 ###
                    else : ### 球打向我方時 ###
                        if y != 415:
                            self.final_x = self.normal("1P",x,y,speed_x,speed_y,self.vframe) ### 球的實際落點 ###     
        else: ### 2P ###
            if len(self.ball_postition_history) > 1 :
                self.ball_x_move = self.ball_postition_history[-1][0] - self.ball_postition_history[-2][0]
                self.ball_y_move = self.ball_postition_history[-1][1] - self.ball_postition_history[-2][1]
                if scene_info["ball_speed"][0] == 0:
                    self.status=0
                    self.vframe=100
                else:
                    self.status = scene_info["ball_speed"][1]/scene_info["ball_speed"][0]
                if  self.status != 0: ### 因為球每100個frame會+1速 所以計算球在多少frame會加速 ###
                    x = self.ball_postition_history[-1][0]
                    y = self.ball_postition_history[-1][1]
                    speed_x = scene_info["ball_speed"][0]
                    speed_y = scene_info["ball_speed"][1]
                    if abs(self.ball_speed_y_history[-1]) - abs(self.ball_speed_y_history[-2])==0:
                        self.vframe = self.vframe - 1
                    else:
                        self.vframe = 100
                    if self.ball_y_move > 0 : ### 球打向對方時 ###
                        self.cut_predict = self.cut("2P",x,y,speed_x,speed_y,self.vframe)
                        self.normal_predict = self.normal("2P",x,y,speed_x,speed_y,self.vframe)
                        self.back_predict = self.back("2P",x,y,speed_x,speed_y,self.vframe)
                        self.final_x = round(( self.cut_predict + self.normal_predict + self.back_predict )/3) ### 球的預測落點 ###
                    else : ### 球打向我方時 ###
                        if y != 80:
                            self.final_x = self.normal("2P",x,y,speed_x,speed_y,self.vframe) ### 球的實際落點 ###
        if platform_center_x <  self.final_x : ### 板子向右移 ###
          self.resault="MOVE_RIGHT" 
        elif platform_center_x >  self.final_x: ### 板子向左移 ###
          self.resault="MOVE_LEFT"
        else: ### 板子不動 ###
          self.resault="NONE"     
        return self.resault
    @staticmethod    
    def apd(self,data,data2):
        self.ball_postition_history.append(data)
        self.ball_speed_y_history.append(data2)
    def reset(self):
        """
        Reset the self.status
        """
        self.ball_served = False
        
    def cut(self,who,x,y,speed_x,speed_y,vframe): ### 對方正向(切球)的預測落點 ###
        final_predict = 0
        while(True):
            x = x + speed_x
            y = y + speed_y
            vframe = vframe - 1
            if vframe == 0 :
                if speed_x > 0 :
                    speed_x = speed_x + 1
                else:
                    speed_x = speed_x - 1
                if speed_y > 0 :
                    speed_y = speed_y + 1
                else:
                    speed_y = speed_y - 1
            if x >= 195 :
                x = 195
                speed_x = -speed_x
            if x <= 0 :
                x = 0
                speed_x = -speed_x                 
            if y >= 415 :
                y = 415
                if who == "1P" :
                    final_predict = x
                    break
                else :
                    if abs(speed_x)-abs(speed_y) == 0 :
                        if speed_x > 0 :
                            speed_x = speed_x + 3
                        else : 
                            speed_x = speed_x - 3
                        speed_y = -speed_y
                    else:
                        speed_y = -speed_y
            if y <= 80 :
                y = 80
                if who == "1P" :
                    if abs(speed_x)-abs(speed_y) == 0 :
                        if speed_x > 0 :
                            speed_x = speed_x + 3
                        else : 
                            speed_x = speed_x - 3
                        speed_y = -speed_y
                    else:
                        speed_y = -speed_y
                else :
                    final_predict = x
                    break
        return final_predict
    def normal(self,who,x,y,speed_x,speed_y,vframe): ### 對方不動(正常)的預測落點 ###
        final_predict = 0
        while(True):
            x = x + speed_x
            y = y + speed_y
            vframe = vframe - 1
            if vframe == 0 :
                if speed_x > 0 :
                    speed_x = speed_x + 1
                else:
                    speed_x = speed_x - 1
                if speed_y > 0 :
                    speed_y = speed_y + 1
                else:
                    speed_y = speed_y - 1
            if x >= 195 :
                x = 195
                speed_x = -speed_x
            if x <= 0 :
                x = 0
                speed_x = -speed_x             
            if y >= 415 :
                y = 415
                if who == "1P" :
                    final_predict = x
                    break
                else :
                    if speed_x > 0:
                        speed_x = abs(speed_y)
                    else:
                        speed_x = -abs(speed_y)
                    speed_y = -speed_y
            if y <= 80 :
                y = 80
                if who == "1P" :
                    if speed_x > 0:
                        speed_x = abs(speed_y)
                    else:
                        speed_x = -abs(speed_y)
                    speed_y = -speed_y
                else :
                    final_predict = x
                    break
        return final_predict
    def back(self,who,x,y,speed_x,speed_y,vframe): ### 對方反向(反打)的預測落點 ###
        final_predict = 0
        while(True):
            x = x + speed_x
            y = y + speed_y
            vframe = vframe - 1
            if vframe == 0 :
                if speed_x > 0 :
                    speed_x = speed_x + 1
                else:
                    speed_x = speed_x - 1
                if speed_y > 0 :
                    speed_y = speed_y + 1
                else:
                    speed_y = speed_y - 1
            if x >= 195 :
                x = 195
                speed_x = -speed_x
            if x <= 0 :
                x = 0
                speed_x = -speed_x                 
            if y >= 415 :
                y = 415
                if who == "1P" :
                    final_predict = x
                    break
                else :
                    if speed_x > 0:
                        speed_x = -abs(speed_y)
                    else:
                        speed_x = abs(speed_y)
                    speed_y = -speed_y
            if y <= 80 :
                y = 80
                if who == "1P" :
                    if speed_x > 0:
                        speed_x = -abs(speed_y)
                    else:
                        speed_x = abs(speed_y)
                    speed_y = -speed_y
                else :
                    final_predict = x
                    break
        return final_predict
