from Utils import get_car_facing_vector, Vector3, clamp
import math

TEAM0_POSTS = [[893, -5120], [-893, -5120]]
TEAM1_POSTS = [[893, 5120], [-893, 5120]]


def get_in_shot_position(agent):
    my_car = agent.game.my_car
    ball = agent.game.ball
    goal_y = 5120
    if agent.game.team == 1:
        goal_y = -5120

    goal_to_ball = Vector3(0-ball.pos.x, goal_y-ball.pos.y, 0)

    unit_goal_to_ball = goal_to_ball.to_unit_vector()

    #good_shot_position = vec3(ball.pos.x+unit_ball_to_goal.x*3000, ball.pos.y+unit_ball_to_goal.y*3000, 92.75)

    good_shot_position = Vector3(ball.pos.x-unit_goal_to_ball.x*3000, ball.pos.y-unit_goal_to_ball.y*3000, 92.75)

    #check if the pos is out of the map cuz that's bad haha
    #https://i.imgur.com/urtkm1t.png
    if good_shot_position.x > 4096:
        AB = ball.pos.x-4096
        CD = ball.pos.y-good_shot_position.y
        AC = ball.pos.x-good_shot_position.x
        
        BE = (AB*CD)/AC
        
        magnitude = math.sqrt(AB**2+BE**2)
        good_shot_position = Vector3(ball.pos.x-unit_goal_to_ball.x*magnitude, ball.pos.y-unit_goal_to_ball.y*magnitude, 92.75)
    if good_shot_position.x < -4096:
        AB = -4096-ball.pos.x
        CD = good_shot_position.y-ball.pos.y
        AC = good_shot_position.x-ball.pos.x

        BE = (AB*CD)/AC

        magnitude = math.sqrt(AB**2+BE**2)
        good_shot_position = Vector3(ball.pos.x-unit_goal_to_ball.x*magnitude, ball.pos.y-unit_goal_to_ball.y*magnitude, 92.75)

    if good_shot_position.y > 5120:
        AB = 5120-ball.pos.y
        CD = good_shot_position.x-ball.pos.x
        AC = good_shot_position.y-ball.pos.y

        BE = (AB*CD)/AC

        magnitude = math.sqrt(AB**2+BE**2)
        good_shot_position = Vector3(ball.pos.x-unit_goal_to_ball.x*magnitude, ball.pos.y-unit_goal_to_ball.y*magnitude, 92.75)
        
    if good_shot_position.y < -5120:
        AB = -5120-ball.pos.y
        CD = good_shot_position.x-ball.pos.x
        AC = good_shot_position.y-ball.pos.y

        BE = (AB*CD)/AC

        magnitude = math.sqrt(AB**2+BE**2)
        good_shot_position = Vector3(ball.pos.x-unit_goal_to_ball.x*magnitude, ball.pos.y-unit_goal_to_ball.y*magnitude, 92.75)


   # good_shot_position = vec3(ball.pos.x-unit_goal_to_ball.x*3000, ball.pos.y-unit_goal_to_ball.y*3000, 92.75)
    
    delta_local = my_car.get_car_facing_vector()

    phi = math.atan2(delta_local.y, delta_local.x)

    if agent.debug_mode:
        r = 200
        #drawing shot position
        x = Vector3(r,0,0)
        y = Vector3(0,r,0)
        z = Vector3(0,0,r)

        purple = agent.renderer.create_color(255, 230, 30, 230)
        agent.renderer.draw_line_3d(my_car.pos.to_array(), good_shot_position.to_array(), purple)

        agent.renderer.draw_line_3d((good_shot_position - x).to_array(), (good_shot_position + x).to_array(), purple)
        agent.renderer.draw_line_3d((good_shot_position - y).to_array(), (good_shot_position + y).to_array(), purple)
        agent.renderer.draw_line_3d((good_shot_position - z).to_array(), (good_shot_position + z).to_array(), purple)

    
    car_to_ball = my_car.pos-ball.pos

    agent.controls.steer = clamp(2.5 * phi, -1.0, 1.0)
    if phi > 1 or phi < -1:
        agent.controls.handbrake = True
    elif phi < 0.001 and phi > -0.001 and car_to_ball.get_magnitude() > my_car.velocity.get_magnitude():
        agent.controls.boost = True
        agent.controls.throttle = 1.0
    else:
        agent.controls.handbrake = False
        agent.controls.throttle = 0.5
        agent.controls.boost = False
    return agent.controls

def calc_shot(agent, ball, draw):
    my_car = agent.game.my_car
    posts = []
    if agent.game.team == 0:
        posts = TEAM1_POSTS
    else:
        posts = TEAM0_POSTS
    

    
    

    angle0 = math.atan2(ball.pos.y-posts[0][1], ball.pos.x-posts[0][0])
    angle1 = math.atan2(ball.pos.y-posts[1][1], ball.pos.x-posts[1][0])

    angle_car_ball = math.atan2((my_car.pos.y-ball.pos.y),(my_car.pos.x-ball.pos.x))

    if draw and agent.debug_mode:
        agent.renderer.draw_string_2d(5, 20, 1, 1, str(angle0), agent.renderer.black())
        agent.renderer.draw_string_2d(5, 40, 1, 1, str(angle1), agent.renderer.black())
        agent.renderer.draw_string_2d(5, 60, 1, 1, str(angle_car_ball), agent.renderer.black())



    if angle_car_ball > angle0 and angle_car_ball < angle1 and my_car.pos.y < ball.pos.y and agent.game.team == 0:
        agent.in_shot_position = True
    elif angle_car_ball < angle0 and angle_car_ball > angle1 and my_car.pos.y > ball.pos.y and agent.game.team == 1:
        agent.in_shot_position = True
    else:
        agent.in_shot_position = False
    return agent.in_shot_position