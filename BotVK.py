DEBUG_MODE = False


import math
import time

from Utils import Vector2, Vector3, get_car_facing_vector, get_closest_boost, distance2D
from Shooting import calc_shot, get_in_shot_position
from States import kick_off, defense, offense, get_boost

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator


from RLUtilities.GameInfo import GameInfo
from RLUtilities.Simulation import Ball
from RLUtilities.LinearAlgebra import dot, clip, vec3, norm
from RLUtilities.Maneuvers import AirDodge
from RLUtilities.controller_input import controller



TEAM0_POSTS = [[893, -5120], [-893, -5120]]
TEAM1_POSTS = [[893, 5120], [-893, 5120]]

class BotVK(BaseAgent):

    def __init__(self, name, team, index):
        #This runs once before the bot starts up
        self.dodgeTimer = 0
        self.dodgeState = 0
        self.info = GameInfo(index, team)
        self.controls = SimpleControllerState()
        self.state = 'kickOff'
        self.start = time.time()
        self.in_shot_position = False
        self.index = index
        self.debug_mode = DEBUG_MODE
        

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        if self.debug_mode:
            self.renderer.begin_rendering()
        self.info.read_packet(packet)
        
        if packet.game_info.is_kickoff_pause:
            self.state = 'kickOff'
        
        if self.state == 'none':
            self.get_new_state(packet)
            # put the car in the middle of the field
            
        
        elif self.state == 'defense' or self.state == 'offense':
            self.clear_ball(False)
        elif self.state == 'kickOff':
            self.kick_off(packet)
        elif self.state == 'get_boost':
            get_boost(self, packet)

        if self.debug_mode:
            self.debug_renderer(packet)
            self.renderer.end_rendering()
        return self.controls

    def debug_renderer(self, packet):
        


         # make a copy of the ball's info that we can change
        b = Ball(self.info.ball)
        ball = self.info.ball
        car = self.info.my_car
        ball_predictions = []
        for i in range(180):

            # simulate the forces acting on the ball for 1 frame
            b.step(1.0 / 60.0)

            # and add a copy of new ball position to the list of predictions
            ball_predictions.append(vec3(b.pos))

        red = self.renderer.create_color(255, 255, 30, 30)
        self.renderer.draw_polyline_3d(ball_predictions, red)

        # drawing
        self.renderer.draw_string_2d(5, 30, 1, 1, str(norm(self.info.my_car.vel)), self.renderer.black())
        self.renderer.draw_string_2d(5, 20, 1, 1, str(norm(ball.pos-car.pos)), self.renderer.black())
        self.renderer.draw_string_2d(5, 5, 1, 1, self.state, self.renderer.black())
        # self.renderer.draw_string_2d(5, 15, 1, 1, str(lisp[0]), self.renderer.black())
        # self.renderer.draw_string_2d(5, 25, 1, 1, str(lisp[1]), self.renderer.black())
        # self.renderer.draw_string_2d(5, 35, 1, 1, str(lisp[2]), self.renderer.black())

        


        ball_location = packet.game_ball.physics.location
        posts = []
        if self.info.team == 0:
            posts = TEAM1_POSTS
        else:
            posts = TEAM0_POSTS

        color = self.renderer.red()
        if self.in_shot_position:
            color = self.renderer.green()
        
        self.renderer.draw_line_3d([posts[0][0], posts[0][1], 92.75], [ball_location.x, ball_location.y, ball_location.z], self.renderer.black())
        self.renderer.draw_line_3d([posts[1][0], posts[1][1], 92.75], [ball_location.x, ball_location.y, ball_location.z], self.renderer.black())
        
        self.renderer.draw_line_3d([ball_location.x, ball_location.y, ball_location.z], [ball_location.x+(ball_location.x-posts[0][0]), ball_location.y+(ball_location.y-posts[0][1]), 92.75], color)
        self.renderer.draw_line_3d([ball_location.x, ball_location.y, ball_location.z], [ball_location.x+(ball_location.x-posts[1][0]), ball_location.y+(ball_location.y-posts[1][1]), 92.75], color)

        self.renderer.draw_line_3d([0, -5120, 92.75], [ball_location.x, ball_location.y, 92.75], color)

        

    def get_new_state(self, packet: GameTickPacket):
        ball = self.info.ball
        if ball.pos[1] < 0 and self.info.team == 0:
            self.state = 'defense'
        elif ball.pos[1] > 0 and self.info.team == 1:
            self.state = 'defense'
        else:
            self.state = 'offense' 

    def kick_off(self, packet: GameTickPacket):
        if packet.game_info.seconds_elapsed-packet.game_ball.latest_touch.time_seconds < 1:
            self.state = 'none'

        self.clear_ball(True)



    def clear_ball(self, kick_off):
        self.in_shot_position = calc_shot(self)
        if not self.in_shot_position and not kick_off:
            self.controller_state = get_in_shot_position(self)
            return

        ball = self.info.ball
        car = self.info.my_car

        # the vector from the car to the ball in local coordinates:
        # delta_local[0]: how far in front of my car
        # delta_local[1]: how far to the left of my car
        # delta_local[2]: how far above my car
        delta_local = dot(ball.pos - car.pos, car.theta)
        # the angle between the direction the car is facing
        # and the in-plane local position of the ball
        phi = math.atan2(delta_local[1], delta_local[0])

        speed = norm(car.vel)

        
        
        self.dodgeTimer += 0.01666

        start = 0

        if kick_off:
            start = 3
        else:
            start = 1/3

        #dodge earlier when kick_off so you launch ball slightly in the air
        if norm(ball.pos-car.pos) < speed*start:
            if self.dodgeTimer > 2:
                self.dodgeState = 0
                self.dodgeTimer = 0
            if self.dodgeState == 0:
                self.dodgeState = 1
                self.dodgeTimer == 0
                self.action = AirDodge(car, 0.1, ball.pos)
                return
            else:
                self.action.step(0.01666)
                self.controls = self.action.controls
                
                return 

        # a simple steering controller that is proportional to phi
        self.controls.steer = clip(2.5 * phi, -1.0, 1.0)
        if phi > 2.5 or phi < -2.5:

            self.controls.handbrake = True
        elif phi < 0.1 and phi > -0.1:
            self.controls.boost = True
            self.controls.throttle = 1.0
        else:
            self.controls.handbrake = False
            self.controls.throttle = 0.5
            self.controls.boost = False
        # just set the throttle to 1 so the car is always moving forward
        



    def get_boost(self, packet: GameTickPacket) -> SimpleControllerState:
        my_car = self.info.my_car
        field_info = self.get_field_info()
        boost = field_info.boost_pads[get_closest_boost(field_info, my_car, packet)]
        boost_location = Vector2(boost.location.x, boost.location.y)
        car_location = Vector2(my_car.physics.location.x, my_car.physics.location.y)
        car_direction = get_car_facing_vector(my_car)
        car_to_boost = boost_location - car_location

        steer_correction_radians = car_direction.correction_to(car_to_boost)

        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -1.0  # Negative value for a turn to the left.
        else:
            turn = 1.0
        self.controller_state.throttle = 1.0
        self.controller_state.steer = turn
        self.controller_state.boost = True
        return self.controller_state
    





