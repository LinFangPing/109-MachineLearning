"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

def ml_loop():
    comm.ml_ready()

    ball_postition_history=[]
    final_x=75
    while True:
        scene_info = comm.get_scene_info()
        platform_center_x=scene_info.platform[0]
        ball_postition_history.append(scene_info.ball)
        if len(ball_postition_history) > 1 :
            ball_x_move = ball_postition_history[-1][0] - ball_postition_history[-2][0]
            ball_y_move = ball_postition_history[-1][1] - ball_postition_history[-2][1]
            ball_platform_high = 400 - ball_postition_history[-1][1]
            if ball_y_move>0 :
                if  ball_platform_high <196 :
                    if ball_x_move > 0 : #right
                        final_x = ball_postition_history[-1][0] + ball_platform_high
                    else : #left
                        final_x = ball_postition_history[-1][0] - ball_platform_high
                else:
                    final_x = 100
            else :
                final_x = 100
            print(str(ball_postition_history[-1][0])+" ; "+str(ball_postition_history[-1][1])+" ; "+str(final_x))
            if  platform_center_x +20 >  final_x:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if  platform_center_x+20 <  final_x:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)    
