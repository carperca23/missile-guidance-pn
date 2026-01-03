import numpy as np

class Target:
    def __init__(self, x, y, speed, heading):
        self.pos = np.array([float(x), float(y)])
        self.speed = float(speed)
        self.heading = np.radians(heading)
        self.vel = np.array([0.0, 0.0])
        
        self.max_g = 9.0  
        self.steering_input = 0.0 

    def update(self, dt):

        max_turn_rate = (self.max_g * 9.81) / self.speed
        
        actual_turn_rate = self.steering_input * max_turn_rate
        self.heading += actual_turn_rate * dt
        
        self.vel = np.array([
            self.speed * np.cos(self.heading),
            self.speed * np.sin(self.heading)
        ])
        self.pos += self.vel * dt

    def set_steering(self, direction):
        self.steering_input = direction

    def get_state(self):
        return self.pos.copy(), self.vel.copy()