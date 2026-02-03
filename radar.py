import numpy as np

class Radar:
    def __init__(self, target, scan_rate=20.0):
        self.target = target
        self.scan_interval = 1.0 / scan_rate
        self.timer = 0.0
        self.sigma_range = 15.0
        self.sigma_azimuth = np.radians(0.5)

    def get_raw_measurement(self, missile_pos, dt):
        self.timer += dt
        if self.timer >= self.scan_interval:
            self.timer = 0.0
            t_pos, _ = self.target.get_state()            
            relative_pos = t_pos - missile_pos
            r = np.linalg.norm(relative_pos) + np.random.normal(0, self.sigma_range)
            az = np.atan2(relative_pos[1], relative_pos[0]) + np.random.normal(0, self.sigma_azimuth)
            return np.array([r, az])
        return None