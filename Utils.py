import math

from rlbot.utils.structures.quick_chats import QuickChats

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        
        self.x = x
        self.y = y
        self.z = z

    def __add__(self,vector):
        return Vector3(self.x+vector.x, self.y+vector.y, self.z+vector.z)
    def __sub__(self,vector):
        return Vector3(self.x-vector.x, self.y-vector.y, self.z-vector.z)
    def __mul__(self,vector):
        return self.x*vector.x + self.y*vector.y + self.z*vector.z
    def get_magnitude(self): 
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z**2)
    def to_unit_vector(self):
        magnitude = self.get_magnitude()
        return Vector3(self.x/magnitude, self.y/magnitude, self.z/magnitude)
    def to_array(self):
        return [self.x, self.y, self.z]
    def get_2d_angle(self):
        return math.atan2(self.y, -self.x)
    def rotate(self, degrees):
        newVector = Vector3(self.x, self.y, self.z)
        #y
        newVector.z = newVector.z*math.cos(degrees.y)-newVector.x*math.sin(degrees.y)
        newVector.x = newVector.z*math.sin(degrees.y)+newVector.x*math.cos(degrees.y)
        #z
        newVector.x = newVector.x*math.cos(degrees.z)-newVector.y*math.sin(degrees.z)
        newVector.y = newVector.x*math.sin(degrees.z)+newVector.y*math.cos(degrees.z)
        #x
        newVector.y = newVector.y*math.cos(degrees.x)-newVector.z*math.sin(degrees.x)
        newVector.z = newVector.y*math.sin(degrees.x)+newVector.z*math.cos(degrees.x)
        return newVector

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

def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    else:
        return value

class quickChat:
    team0_goals = 0
    team1_goals = 0

    @staticmethod
    def run(agent, packet):
        new_team0_goals = 0
        new_team1_goals = 0
        for i, car in enumerate(packet.game_cars):
            if car.team == 0:
                new_team0_goals += car.score_info.goals
            else:
                new_team1_goals += car.score_info.goals
        
        if quickChat.team0_goals != new_team0_goals:
            quickChat.team0_goals = new_team0_goals
            if agent.game.team == 0:
                agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Reactions_Calculated)
            else:
                agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Compliments_NiceShot)
        elif quickChat.team1_goals != new_team1_goals:
            quickChat.team1_goals = new_team1_goals
            if agent.game.team == 1:
                agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Reactions_Calculated)
            else:
                agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Compliments_NiceShot)



def get_car_facing_vector(car):
    pitch = float(car.rotation.pitch)
    yaw = float(car.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector2(facing_x, facing_y)