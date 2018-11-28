import math
from Utils import Vector3

class Game:
    def __init__(self, index, team, field_info):
        self.index = index
        self.team = team
        self.ball = None
        self.my_car = None
        self.cars = []
        self.field_info = field_info
        self.boosts = [None] * len(field_info.boost_pads)
        self.info = None
    
    def load_packet(self, packet, ball_predictions):
        self.ball = Ball(packet.game_ball, ball_predictions)
        self.my_car = Car(packet.game_cars[self.index])
        self.num_cars = packet.num_cars
        #loading in boost
        for i, boost in enumerate(self.field_info.boost_pads):
            #self.boosts[i] = 'hai'
            self.boosts[i] = BoostPad(boost, packet.game_boosts[i])
            
    def get_closest_boost(self):
        closest_boost = None
        closest_boost_distance = 10000
        for boost in self.boosts:
            if not boost.filled:
                continue
            if not boost.big:
                continue
            distance = boost.pos-self.my_car.pos
            if distance.get_magnitude() < closest_boost_distance:
                closest_boost = boost
                closest_boost_distance = distance.get_magnitude()
        
        return closest_boost
class BoostPad:
    def __init__(self, field_info, packet_info):
        self.pos = Vector3(field_info.location.x, field_info.location.y, field_info.location.z)
        self.big = field_info.is_full_boost
        self.filled = packet_info.is_active
        self.timer = packet_info.timer


class Car:
    def __init__(self, car):
        self.pos = Vector3(car.physics.location.x, car.physics.location.y, car.physics.location.z)
        self.rotation = car.physics.rotation
        self.velocity = Vector3(car.physics.velocity.x, car.physics.velocity.y, car.physics.velocity.z)
        self.ang_velocity = Vector3(car.physics.angular_velocity.x, car.physics.angular_velocity.y, car.physics.angular_velocity.z)
        self.is_demolished = car.is_demolished
        self.has_wheel_contact = car.has_wheel_contact
        self.is_super_sonic = car.is_super_sonic
        self.jumped = car.jumped
        self.double_jumped = car.double_jumped
        self.name = car.name
        self.boost = car.boost
        self.score_info = car.score_info
    
    def get_car_facing_vector(self):
        pitch = float(self.rotation.pitch)
        yaw = float(self.rotation.yaw)

        facing_x = math.cos(pitch) * math.cos(yaw)
        facing_y = math.cos(pitch) * math.sin(yaw)

        return Vector3(facing_x, facing_y, 0)

class Ball:
    def __init__(self, ball, ball_predictions):
        self.pos = Vector3(ball.physics.location.x, ball.physics.location.y, ball.physics.location.z)
        self.rotation = ball.physics.rotation
        self.velocity = Vector3(ball.physics.velocity.x, ball.physics.velocity.y, ball.physics.velocity.z)
        self.ang_velocity = Vector3(ball.physics.angular_velocity.x, ball.physics.angular_velocity.y, ball.physics.angular_velocity.z)
        self.latest_touch = ball.latest_touch
        self.ball_predictions = ball_predictions
    def predict(self, seconds):
        frame = round(seconds*60)
        return self.ball_predictions[frame]


