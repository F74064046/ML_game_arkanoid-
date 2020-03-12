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
        else:#遊戲中
            ball_x = scene_info.ball[0]
            platfrom_x = scene_info.platform[0]
            if ball_x > platfrom_x:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            else :
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)

