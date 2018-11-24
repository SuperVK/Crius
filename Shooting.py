from Utils import get_car_facing_vector, unit_vector, get_magnitude
from RLUtilities.LinearAlgebra import vec2, vec3, dot, clip, norm
import math

TEAM0_POSTS = [[893, -5120], [-893, -5120]]
TEAM1_POSTS = [[893, 5120], [-893, 5120]]


def get_in_shot_position(agent):
    car = agent.info.my_car
    ball = agent.info.ball
    goal_y = 5120
    index = -1
    if agent.info.team == 1:
        index = 1
        goal_y = -5120

    goal_to_ball = vec2(0-ball.pos[0], goal_y-ball.pos[1])

    unit_goal_to_ball = unit_vector(goal_to_ball)

    #good_shot_position = vec3(ball.pos[0]+unit_ball_to_goal[0]*3000, ball.pos[1]+unit_ball_to_goal[1]*3000, 92.75)

    good_shot_position = vec3(ball.pos[0]-unit_goal_to_ball[0]*3000, ball.pos[1]-unit_goal_to_ball[1]*3000, 92.75)

    #check if the pos is out of the map cuz that's bad haha
    #https://i.imgur.com/urtkm1t.png
    if good_shot_position[0] > 4096:
        AB = ball.pos[0]-4096
        CD = ball.pos[1]-good_shot_position[1]
        AC = ball.pos[0]-good_shot_position[0]
        
        BE = (AB*CD)/AC
        
        magnitude = math.sqrt(AB**2+BE**2)
        good_shot_position = vec3(ball.pos[0]-unit_goal_to_ball[0]*magnitude, ball.pos[1]-unit_goal_to_ball[1]*magnitude, 92.75)
    if good_shot_position[0] < -4096:
        AB = -4096-ball.pos[0]
        CD = good_shot_position[1]-ball.pos[1]
        AC = good_shot_position[0]-ball.pos[0]

        BE = (AB*CD)/AC

        magnitude = math.sqrt(AB**2+BE**2)
        good_shot_position = vec3(ball.pos[0]-unit_goal_to_ball[0]*magnitude, ball.pos[1]-unit_goal_to_ball[1]*magnitude, 92.75)

    if good_shot_position[1] > 5120:
        AB = 5120-ball.pos[1]
        CD = good_shot_position[0]-ball.pos[0]
        AC = good_shot_position[1]-ball.pos[1]

        BE = (AB*CD)/AC

        magnitude = math.sqrt(AB**2+BE**2)
        good_shot_position = vec3(ball.pos[0]-unit_goal_to_ball[0]*magnitude, ball.pos[1]-unit_goal_to_ball[1]*magnitude, 92.75)
        
    if good_shot_position[1] < -5120:
        AB = -5120-ball.pos[1]
        CD = good_shot_position[0]-ball.pos[0]
        AC = good_shot_position[1]-ball.pos[1]

        BE = (AB*CD)/AC

        magnitude = math.sqrt(AB**2+BE**2)
        good_shot_position = vec3(ball.pos[0]-unit_goal_to_ball[0]*magnitude, ball.pos[1]-unit_goal_to_ball[1]*magnitude, 92.75)


   # good_shot_position = vec3(ball.pos[0]-unit_goal_to_ball[0]*3000, ball.pos[1]-unit_goal_to_ball[1]*3000, 92.75)
    delta_local = dot(good_shot_position - car.pos, car.theta)
    phi = math.atan2(delta_local[1], delta_local[0])

    if agent.debug_mode:
        r = 200
        #drawing shot position
        x = vec3(r,0,0)
        y = vec3(0,r,0)
        z = vec3(0,0,r)

        purple = agent.renderer.create_color(255, 230, 30, 230)
        agent.renderer.draw_line_3d(car.pos, good_shot_position, purple)

        agent.renderer.draw_line_3d(good_shot_position - x, good_shot_position + x, purple)
        agent.renderer.draw_line_3d(good_shot_position - y, good_shot_position + y, purple)
        agent.renderer.draw_line_3d(good_shot_position - z, good_shot_position + z, purple)
    
    car_to_ball = car.pos-ball.pos

    agent.controls.steer = clip(2.5 * phi, -1.0, 1.0)
    if phi > 1 or phi < -1:
        agent.controls.handbrake = True
    elif phi < 0.001 and phi > -0.001 and get_magnitude(car_to_ball) > norm(car.vel):
        agent.controls.boost = True
        agent.controls.throttle = 1.0
    else:
        agent.controls.handbrake = False
        agent.controls.throttle = 0.5
        agent.controls.boost = False
    return agent.controls

def calc_shot(agent):
    ball = agent.info.ball
    car = agent.info.my_car
    posts = []
    if agent.info.team == 0:
        posts = TEAM1_POSTS
    else:
        posts = TEAM0_POSTS
    
    # the vector from the car to the ball in local coordinates:
    # delta_local[0]: how far in front of my car
    # delta_local[1]: how far to the left of my car
    # delta_local[2]: how far above my car
    delta_local = dot(ball.pos - car.pos, car.theta)

    A = ball.pos
    B = vec2(ball.pos[0]+(ball.pos[0]-posts[0][0]), ball.pos[1]+(ball.pos[1]-posts[0][1]))
    C = vec2(ball.pos[0]+(ball.pos[0]-posts[1][0]), ball.pos[1]+(ball.pos[1]-posts[1][1]))

    angle0 = math.atan((A[0]-B[0])/(A[1]-B[1]))
    angle1 = math.atan((A[0]-C[0])/(A[1]-B[1]))
    angle_car_ball = math.atan((ball.pos[0]-car.pos[0])/(ball.pos[1]-car.pos[1]))



    if angle_car_ball > angle0 and angle_car_ball < angle1 and car.pos[1] > ball.pos[1] and agent.info.team == 1:
        agent.in_shot_position = True
    elif angle_car_ball > angle0 and angle_car_ball < angle1 and car.pos[1] < ball.pos[1] and agent.info.team == 0:
        agent.in_shot_position = True
    else:
        agent.in_shot_position = False
    
    return agent.in_shot_position