import numpy as np

class ProportionalNavigation:
    def __init__(self, N):
        self.N = N
        self.lambda_anterior = 0
    
    def get_guidance_command(self, t_pos, t_vel, m_pos, m_vel, dt):
        R = t_pos - m_pos
        lambda_actual = np.atan2(R[1], R[0])
        vc = -np.dot(t_vel-m_vel, R/np.linalg.norm(R))

        delta_lambda = lambda_actual - self.lambda_anterior
        
        if delta_lambda > np.pi:
            delta_lambda -= 2 * np.pi
        elif delta_lambda < -np.pi:
            delta_lambda += 2 * np.pi
            
        rotation_rate = delta_lambda/dt
        self.lambda_anterior = lambda_actual

        return self.N*vc*rotation_rate

