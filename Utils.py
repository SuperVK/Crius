import math

from RLUtilities.LinearAlgebra import vec2, vec3, dot, clip


class Vector3:
    def __init__(self, x, y, z):
        
        self.x = x
        self.y = y
        self.z = z
    def __sub__(self,value):
        return Vector3(self.x-value.x, self.y-value.y, self.z-value.z)
    def __mul__(self,value):
        return self.x*value.x + self.y*value.y + self.z*value.z

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        return Vector2(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        return Vector2(self.x - val.x, self.y - val.y)

    def correction_to(self, ideal):
        # The in-game axes are left handed, so use -x
        current_in_radians = math.atan2(self.y, -self.x)
        ideal_in_radians = math.atan2(ideal.y, -ideal.x)

        correction = ideal_in_radians - current_in_radians

        # Make sure we go the 'short way'
        if abs(correction) > math.pi:
            if correction < 0:
                correction += 2 * math.pi
            else:
                correction -= 2 * math.pi

        return correction
    
def get_closest_boost(field_info, car, packet):
    closest_boost_index = 0
    closest_boost_distance = 10000
    for i, boost in enumerate(field_info.boost_pads):
        if not boost.is_full_boost:
            continue
        if not packet.game_boosts[i].is_active:
            continue
        xErr = abs(boost.location.x - car.physics.location.x)
        yErr = abs(boost.location.y - car.physics.location.y)
        total = xErr + yErr
        if total < closest_boost_distance:
            closest_boost_index = i
            closest_boost_distance = total
    return closest_boost_index


def get_car_facing_vector(car):
    pitch = float(car.theta.pitch)
    yaw = float(car.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector2(facing_x, facing_y)

def distance2D(target_object, our_object):
    if isinstance(target_object,Vector3):
        difference = target_object - our_object
    else:
        difference = target_object.location - our_object.location
    return math.sqrt(difference.data[0]**2 + difference.data[1]**2)

def unit_vector(vector):
    magnitude = get_magnitude(vector)
    return vec2(vector[0]/magnitude, vector[1]/magnitude)

def get_magnitude(vector): 
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)
