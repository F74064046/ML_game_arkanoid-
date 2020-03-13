"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop(): #function的開頭
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False #有沒有發球

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready() #一定要保留 開啟和遊戲核心聯繫的管道

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info() #遊戲的場景資訊

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        # 一個frame只能傳一個指令!!
        if not ball_served: #遊戲開始
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_RIGHT)
            ball_served = True
            ball_last_y = scene_info.ball[1]
            ball_y_dir = "up"
            first_down = False
            final_x = 0
        else:#遊戲中
            #直接用球第一次向下碰到牆壁的位置來預測最後球落在的位置
            ball_x = scene_info.ball[0]
            ball_y = scene_info.ball[1]
            platfrom_x = scene_info.platform[0]
            
            #判斷方向
            if ball_last_y < ball_y : #方向向下
                ball_y_dir = "down"
            else:
                ball_y_dir = "up"
            ball_last_y = ball_y
            

            if ball_y_dir == "down":        
                if ball_x == 0:
                    print(ball_y)
                    gogo = (400 - ball_y)//7
                    #print(gogo)
                    if gogo > 28:
                        gogo = gogo-28
                        final_x = 195 - gogo*7
                    else:
                        final_x = gogo*7
                   
                if ball_x == 195:
                    print(ball_y)
                    gogo = (400 - ball_y)//7
                    #print(gogo)
                    if gogo > 28:
                        gogo = gogo-28
                        final_x = gogo*7
                    else:
                        final_x = 195 - gogo*7
                    
            

            #send instruction
            if ball_y <= 205:#讓板子回歸中間才來的及接球
                if platfrom_x <= 80 and platfrom_x >=100:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                else:
                    if platfrom_x < 80:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    else:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                if platfrom_x+18 <= final_x and platfrom_x + 22 >= final_x:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                else:
                    if platfrom_x+18 < final_x:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    else:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            

