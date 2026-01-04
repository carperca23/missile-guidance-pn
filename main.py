import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from missile import Missile
from target import Target

dt = 0.005
min_dist = float('inf')
objetivo = Target(x=6000, y=6000, speed=400, heading=30)
misil = Missile(x=0, y=0, speed=1205, heading=45, N=5, target=objetivo, dt=dt)

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10000); ax.set_ylim(0, 10000)
ax.set_aspect('equal')

line_target, = ax.plot([], [], 'r--', alpha=0.3)
line_missile, = ax.plot([], [], 'b-', alpha=0.8)
point_target, = ax.plot([], [], 'ro', label="Tú (Avión)")
point_missile, = ax.plot([], [], 'k>', label="Misil")
text_info = ax.text(0.02, 0.95, '', transform=ax.transAxes)

teclas_presionadas = set()

def on_press(event):
    if event.key == 'left': objetivo.set_steering(1)  
    if event.key == 'right': objetivo.set_steering(-1) 

def on_release(event):
    if event.key in ['left', 'right']:
        objetivo.set_steering(0)

fig.canvas.mpl_connect('key_press_event', on_press)
fig.canvas.mpl_connect('key_release_event', on_release)

t_hist_x, t_hist_y = [], []
m_hist_x, m_hist_y = [], []

def update(frame):
    global min_dist

    objetivo.update(dt)
    misil.step(dt)
    
    m_pos, _ = misil.get_state()
    t_pos, _ = objetivo.get_state()
    
    t_hist_x.append(t_pos[0]); t_hist_y.append(t_pos[1])
    m_hist_x.append(m_pos[0]); m_hist_y.append(m_pos[1])
    
    line_target.set_data(t_hist_x, t_hist_y)
    line_missile.set_data(m_hist_x, m_hist_y)
    point_target.set_data([t_pos[0]], [t_pos[1]])
    point_missile.set_data([m_pos[0]], [m_pos[1]])
    
    dist = np.linalg.norm(t_pos - m_pos)
    if dist <= min_dist:
        min_dist = dist
    else:
        print(min_dist)
        exit()
    text_info.set_text(f'Distancia: {dist:.1f}m')
    
    if dist < 10.0:
        text_info.set_text("¡DERRIBADO!")
        ani.event_source.stop()
        print(min_dist)
        
    return line_target, line_missile, point_target, point_missile, text_info

ani = FuncAnimation(fig, update, frames=None, blit=True, interval=20, cache_frame_data=False)
plt.legend()
plt.show()