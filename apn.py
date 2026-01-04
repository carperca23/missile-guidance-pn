import numpy as np

class AugmentedProportionalNavigation:
    def __init__(self, N):
        self.N = N
        self.lambda_anterior = None
    
    def get_guidance_command(self, t_pos, t_vel, t_acc, m_pos, m_vel, dt):
        R = t_pos - m_pos
        dist = np.linalg.norm(R)
        if dist < 1.0: return 0.0
        
        r_unit = R / dist
        lambda_actual = np.atan2(R[1], R[0])

        if self.lambda_anterior is None:
            self.lambda_anterior = lambda_actual
            return 0.0
        
        vc = -np.dot(t_vel - m_vel, r_unit)
        delta_lambda = (lambda_actual - self.lambda_anterior)
        
        if delta_lambda > np.pi: delta_lambda -= 2*np.pi
        elif delta_lambda < -np.pi: delta_lambda += 2*np.pi
            
        rotation_rate = delta_lambda / dt
        self.lambda_anterior = lambda_actual

        normal_los = np.array([-r_unit[1], r_unit[0]])
        at_normal = np.dot(t_acc, normal_los)

        return self.N * vc * rotation_rate + (self.N / 2.0) * at_normal

