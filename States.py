from Utils import Vector2, Vector3, get_car_facing_vector, get_closest_boost, distance2D
import math

def kick_off(agent, packet):
    agent.clear_target(packet, Vector3(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y, packet.game_ball.physics.location.z))

def defense(agent, packet):
    # my_car = packet.game_cars[agent.index]
    # car_location = Vector3(my_car.physics.location.x, my_car.physics.location.y, my_car.physics.location.z)
    # ball_location = Vector3(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y, packet.game_ball.physics.location.z)
    # team = 1
    # at_own_side = False
    # if my_car.team == 0:
    #     team = 1
    #     if car_location.y < 0:
    #         at_own_side = True
    #     else:
    #         at_own_side = False
    # else:
        
    #     team = -1
    #     if car_location.y > 0:
    #         at_own_side = True
    #     else:
    #         at_own_side = False
    # if at_own_side and abs(car_location.y) < abs(ball_location.y):
    #     agent.clear_target(packet, Vector3(4096, -5120*team, 0))
    # else:
    #     agent.clear_target(packet, Vector3(ball_location.x, ball_location.y, ball_location.z))
    pass
    
def offense(agent, packet):
    #gent.clear_target(packet, Vector3(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y, packet.game_ball.physics.location.z))
    pass



    

def get_boost(agent, packet):
    my_car = packet.game_cars[agent.index]
    field_info = agent.get_field_info()
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
    agent.controller_state.throttle = 1.0
    agent.controller_state.steer = turn
    agent.controller_state.boost = True
    return agent.controller_state


