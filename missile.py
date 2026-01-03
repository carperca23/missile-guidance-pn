import numpy as np
from pn import ProportionalNavigation
from target import Target

class Missile:

    def __init__(self, x, y, speed, heading, N, target:Target):
        self.pos = np.array([float(x), float(y)])
        self.speed = float(speed)
        self.heading = np.radians(heading)
        self.pn = ProportionalNavigation(N)
        self.target = target
        self.vel = np.array([speed * np.cos(heading),
                            speed * np.sin(heading)
                            ])

    def step(self, dt):
        t_pos, t_vel = self.target.get_state()
        an = self.pn.get_guidance_command(t_pos, t_vel, self.pos, self.vel, dt)
        max_an = 30 * 9.81
        an = np.clip(an, -max_an, max_an)
        self.heading += (an/self.speed)*dt
        self.vel = np.array([
            self.speed*np.cos(self.heading),
            self.speed*np.sin(self.heading)
        ])
        self.pos += self.vel*dt

    def get_state(self):
        return self.pos.copy(), self.vel.copy()



