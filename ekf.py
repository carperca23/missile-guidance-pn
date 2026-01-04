import numpy as np

class EKF:
    def __init__(self, dt, sigma_range, sigma_azimuth):
        self.dt = dt
        # Estado: [x, y, vx, vy, ax, ay]
        self.x = np.zeros(6) 
        self.P = np.eye(6) * 1000.0
        
        self.F = np.array([
            [1, 0, dt, 0, 0.5*dt**2, 0],
            [0, 1, 0, dt, 0, 0.5*dt**2],
            [0, 0, 1, 0, dt, 0],
            [0, 0, 0, 1, 0, dt],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
        
        q_std = 15.0
        self.Q = np.eye(6) * q_std**2
        
        self.R = np.diag([sigma_range**2, sigma_azimuth**2])

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z, missile_pos):
        x_est, y_est = self.x[0], self.x[1]
        
        rel_x = x_est - missile_pos[0]
        rel_y = y_est - missile_pos[1]
        
        r_est = np.sqrt(rel_x**2 + rel_y**2)
        if r_est < 1.0: return

        h_x = np.array([r_est, np.atan2(rel_y, rel_x)])
        
        H = np.array([
            [rel_x/r_est, rel_y/r_est, 0, 0, 0, 0],
            [-rel_y/r_est**2, rel_x/r_est**2, 0, 0, 0, 0]
        ])
        
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        
        y = z - h_x
        y[1] = (y[1] + np.pi) % (2 * np.pi) - np.pi 
        
        self.x = self.x + K @ y
        self.P = (np.eye(6) - K @ H) @ self.P

    def get_estimate(self):
        return self.x[:2], self.x[2:4], self.x[4:]