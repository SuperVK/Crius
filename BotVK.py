DEBUG_MODE = True


import math
import time


from gameInfo import Game
from Utils import Vector2, Vector3, get_car_facing_vector, quickChat, clamp
from Shooting import calc_shot, get_in_shot_position

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


TEAM0_POSTS = [[893, -5120], [-893, -5120]]
TEAM1_POSTS = [[893, 5120], [-893, 5120]]

class BotVK(BaseAgent):

    def __init__(self, name, team, index):
        #This runs once before the bot starts up
        self.dodgeTimer = 0
        self.dodgeState = 0
        self.index = index
        self.team = team
        self.controls = SimpleControllerState()
        self.state = 'kick_off'
        self.start = time.time()
        self.in_shot_position = False
        self.index = index
        self.debug_mode = DEBUG_MODE
        
    def initialize_agent(self):
        self.game = Game(self.index, self.team, self.get_field_info())

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        if self.debug_mode:
            self.renderer.begin_rendering()
        self.game.load_packet(packet, self.get_ball_prediction_struct())
        calc_shot(self, True)

        quickChat.run(self, packet)

        if packet.game_info.is_kickoff_pause:
            self.state = 'kick_off'
        
        if packet.game_info.seconds_elapsed - packet.game_ball.latest_touch.time_seconds < 0.1:
            self.state = 'none'


        if self.state == 'none':
            self.get_new_state(packet)
            # put the car in the middle of the field
            
        elif self.state == 'getInShotPos':
            if not calc_shot(self, False):
                get_in_shot_position(self)
            else:
                self.state = 'clear_ball'
        elif self.state == 'clear_ball':
            self.clear_ball(False)
        elif self.state == 'kick_off':
            self.kick_off(packet)
        elif self.state == 'get_boost':
            if packet.game_cars[self.index].boost != 100.0: 
                self.get_boost(packet)
            else:
                self.state = 'none'

        if self.debug_mode:
            self.debug_renderer(packet)
            self.renderer.end_rendering()
        return self.controls

    def debug_renderer(self, packet):
        # drawing
        # my_car = self.game.my_car
        # ball = self.game.ball
    
        self.renderer.draw_string_2d(5, 5, 1, 1, self.state, self.renderer.black())
        # self.renderer.draw_string_2d(5, 15, 1, 1, str(lisp[0]), self.renderer.black())
        # self.renderer.draw_string_2d(5, 25, 1, 1, str(lisp[1]), self.renderer.black())
        # self.renderer.draw_string_2d(5, 35, 1, 1, str(lisp[2]), self.renderer.black())

        ball_location = packet.game_ball.physics.location
        posts = []
        if self.game.team == 0:
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
        ball = self.game.ball
        self.in_shot_position = calc_shot(self, False)

        if ball.velocity.z > 750:
            self.state = 'get_boost'
        elif self.in_shot_position:
            self.state = 'clear_ball'
        else:
            self.state = 'getInShotPos'
        

    def kick_off(self, packet: GameTickPacket):
        if packet.game_info.seconds_elapsed-packet.game_ball.latest_touch.time_seconds < 1:
            self.state = 'none'

        self.clear_ball(True)



    def clear_ball(self, kick_off):
        ball = self.game.ball
        my_car = self.game.my_car

        # the vector from the car to the ball in local coordinates:
        # delta_local[0]: how far in front of my car
        # delta_local[1]: how far to the left of my car
        # delta_local[2]: how far above my car
        car_facing = my_car.get_car_facing_vector()
        car_to_ball = ball.pos-my_car.pos

        phi = car_facing.get_2d_angle()-car_to_ball.get_2d_angle()
        # the angle between the direction the car is facing
        # and the in-plane local position of the ball
        

        #speed = my_car.velocity.get_magnitude()

        
        
        self.dodgeTimer += 0.01666


        # if kick_off:
        #     start = 3
        # else:
        #     start = 1/3

        #dodge earlier when kick_off so you launch ball slightly in the air
        # if (ball.pos-my_car.pos).get_magnitude() < speed*start:
        #     if self.dodgeTimer > 2:
        #         self.dodgeState = 0
        #         self.dodgeTimer = 0
        #     if self.dodgeState == 0:
        #         self.dodgeState = 1
        #         self.dodgeTimer == 0
        #         self.action = AirDodge(car, 0.1, ball.pos)
        #         return
        #     else:
        #         self.action.step(0.01666)
        #         self.controls = self.action.controls
                
        #         return 

        # a simple steering controller that is proportional to phi
        self.controls.steer = clamp(2.5 * phi, -1.0, 1.0)
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
        ball = self.game.ball
        my_car = self.game.my_car
        boost = self.game.get_closest_boost()
        car_to_boost = boost.pos - my_car.pos

        car_facing = my_car.get_car_facing_vector()
        car_to_ball = ball.pos-my_car.pos

        phi = car_facing.get_2d_angle()-car_to_ball.get_2d_angle()

        self.controls.steer = clamp(2.5 * phi, -1.0, 1.0)
        if phi > 1 or phi < -1:
            self.controls.handbrake = True
        elif phi < 0.001 and phi > -0.001 and car_to_boost.get_magnitude() > my_car.velocity.get_magnitude():
            self.controls.boost = True
            self.controls.throttle = 1.0
        else:
            self.controls.handbrake = False
            self.controls.throttle = 0.5
            self.controls.boost = False
        return self.controls
    





