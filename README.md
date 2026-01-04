# 🚀 Simulador de Guiado de Misiles con APN

Simulación interactiva en tiempo real de un sistema de guiado de misiles utilizando **Augmented Proportional Navigation (APN)** con filtrado Extended Kalman Filter (EKF) para estimación de estado del objetivo.

##  Descripción

Este proyecto simula un escenario de interceptación donde un misil debe derribar un avión objetivo maniobrable. El sistema implementa técnicas avanzadas de guiado utilizadas en misiles reales:

- **APN (Augmented Proportional Navigation)**: Ley de guiado que anticipa las maniobras del objetivo
- **EKF (Extended Kalman Filter)**: Estimación óptima de posición, velocidad y aceleración del objetivo
- **Radar con ruido realista**: Mediciones imperfectas con errores en rango y azimut
- **Control interactivo**: El jugador controla el avión objetivo intentando evadir el misil

##  Características

- Simulación física realista con límites de maniobra (g's)
- Radar montado en el misil con tasa de escaneo configurable (20 Hz)
- Visualización en tiempo real de trayectorias
- Control interactivo del objetivo con teclado
- Métricas de rendimiento (distancia mínima de aproximación)

##  Requisitos

```bash
pip install numpy matplotlib
```

##  Uso

```bash
python main.py
```

### Controles

- **← Flecha Izquierda**: Girar el avión a la izquierda
- **→ Flecha Derecha**: Girar el avión a la derecha
- **Soltar tecla**: Volar recto

### Objetivo del Juego

**Como jugador (avión rojo)**: Evitar ser derribado realizando maniobras evasivas.

**Victoria**: Hacer que el misil falle (distancia mínima > 10m)

**Derrota**: El misil te alcanza (distancia < 10m)

##  Estructura del Proyecto

```
├── main.py          # Loop principal y visualización
├── missile.py       # Clase del misil con integración de sistemas
├── target.py        # Clase del avión objetivo con física de vuelo
├── apn.py           # Implementación del algoritmo APN
├── ekf.py           # Filtro de Kalman Extendido
└── radar.py         # Simulación de sensor radar
```

##  Algoritmos Implementados

### Augmented Proportional Navigation (APN)

La ley de guiado APN genera comandos de aceleración perpendicular a la línea de visión (LOS):

```
a_n = N × V_c × λ̇ + (N/2) × a_t⊥
```

Donde:
- `N`: Constante de navegación (N=5)
- `V_c`: Velocidad de cierre
- `λ̇`: Tasa de rotación de la LOS
- `a_t⊥`: Aceleración del objetivo perpendicular a la LOS

**Ventaja sobre PN clásico**: El término adicional `(N/2) × a_t⊥` permite anticipar maniobras del objetivo, reduciendo drásticamente el "miss distance".

### Extended Kalman Filter (EKF)

Estima el estado del objetivo a partir de mediciones ruidosas del radar:

**Vector de estado**: `[x, y, vx, vy, ax, ay]`

**Modelo de proceso**: Aceleración constante con ruido

**Mediciones**: Rango y azimut relativos al misil

El EKF realiza dos pasos por cada ciclo:
1. **Predicción**: Propaga el estado usando el modelo dinámico
2. **Actualización**: Corrige la estimación con nuevas mediciones

##  Parámetros Configurables

### En `main.py`:
```python
dt = 0.005                    # Paso de integración (s)
objetivo = Target(
    x=1000,                   # Posición inicial X (m)
    y=4000,                   # Posición inicial Y (m)
    speed=400,                # Velocidad del objetivo (m/s)
    heading=30                # Rumbo inicial (grados)
)
misil = Missile(
    x=0, y=0,                 # Posición inicial (origen)
    speed=1205,               # Velocidad del misil (m/s)
    heading=45,               # Rumbo inicial (grados)
    N=5                       # Constante de navegación APN
)
```

### En `radar.py`:
```python
scan_rate = 20.0              # Frecuencia de escaneo (Hz)
sigma_range = 15.0            # Error en rango (m)
sigma_azimuth = 0.5           # Error en azimut (grados)
```

### En `target.py`:
```python
max_g = 9.0                   # Máximo factor de carga (g's)
```

### En `missile.py`:
```python
max_an = 50 * 9.81            # Máxima aceleración lateral (m/s²)
```

##  Métricas de Rendimiento

Al finalizar la simulación, se muestra:
- **Distancia mínima de aproximación**: Métrica clave de efectividad del guiado
- **Resultado**: "¡DERRIBADO!" si distancia < 10m

##  Conceptos Técnicos

### PN vs APN

| Característica | PN | APN |
|----------------|----|----|
| Contra objetivos no maniobrados | Óptimo | Igual |
| Contra objetivos maniobrados | Reactivo | Predictivo |
| Miss distance típico | Mayor | Menor |
| Complejidad | Baja | Media |
| Requisitos de sensor | Pos + Vel | Pos + Vel + Acel |

### Ventajas del Radar Montado en el Misil

- Mediciones relativas reales (no desde origen fijo)
- Error angular menos crítico al acercarse
- Convergencia del EKF con el tiempo
- Más realista para simulación táctica

### Limitaciones del Modelo Actual

- Velocidad del misil constante (no considera consumo de combustible)
- Modelo de aceleración constante en EKF (objetivos reales son más complejos)
- No hay pérdida de energía del objetivo en giros
- Atmósfera idealizada (sin resistencia del aire variable)

##  Estrategias de Evasión

Para el jugador que controla el objetivo:

1. **Maniobras tempranas**: Cambios de dirección cuando el misil está lejos
2. **Giros sostenidos**: Fuerzas al misil a altas aceleraciones laterales
3. **Cambios de sentido**: Alternar izquierda/derecha para confundir predicción
4. **Timing**: Aprovechar el retardo entre mediciones del radar (50ms)


##  Contribuciones

Mejoras sugeridas:
- [ ] Añadir múltiples objetivos
- [ ] Implementar contramedidas (chaff/flares)
- [ ] Modo de persecución pura para comparación
- [ ] Telemetría detallada en tiempo real
- [ ] Terreno 3D
- [ ] Diferentes tipos de sensores (IR, óptico)


**Nota**: Esta es una simulación simplificada con fines educativos. Los sistemas reales de guiado de misiles son significativamente más complejos.