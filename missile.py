import numpy as np
from apn import AugmentedProportionalNavigation
from radar import Radar
from ekf import EKF

class Missile:
    def __init__(self, x, y, speed, heading, N, target, dt):
        self.pos = np.array([float(x), float(y)])
        self.speed = float(speed)
        self.heading = np.radians(heading)
        self.vel = np.array([speed * np.cos(self.heading), speed * np.sin(self.heading)])
        
        self.apn = AugmentedProportionalNavigation(N)
        self.radar = Radar(target)
        
        self.ekf = EKF(dt, 
                       sigma_range=self.radar.sigma_range, 
                       sigma_azimuth=self.radar.sigma_azimuth)
        self.is_tracking = False

    def step(self, dt):
        z = self.radar.get_raw_measurement(self.pos, dt)
        self.ekf.predict()
        
        if z is not None:
            if not self.is_tracking:
                r, az = z[0], z[1]
                self.ekf.x = np.array([r*np.cos(az), r*np.sin(az), 200.0, 200.0, 0, 0])
                self.is_tracking = True
            self.ekf.update(z, self.pos)

        t_pos_est, t_vel_est, t_acc_est = self.ekf.get_estimate()
        
        an = self.apn.get_guidance_command(t_pos_est, t_vel_est, t_acc_est, self.pos, self.vel, dt)
        
        max_an = 50 * 9.81 
        an = np.clip(an, -max_an, max_an)
        
        self.heading += (an/self.speed)*dt
        self.vel = np.array([self.speed*np.cos(self.heading), self.speed*np.sin(self.heading)])
        self.pos += self.vel*dt

    def get_state(self):
        return self.pos.copy(), self.vel.copy()