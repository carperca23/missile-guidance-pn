# Simulador de Guiado de Misiles con Navegación Proporcional

Un simulador interactivo en Python que implementa un sistema de guiado de misiles utilizando el algoritmo de **Navegación Proporcional (Proportional Navigation)** para interceptar un objetivo móvil que puedes controlar en tiempo real.

## Descripción

Este proyecto simula el comportamiento de un misil que persigue un objetivo (avión) utilizando uno de los algoritmos de guiado más utilizados en sistemas de defensa reales. Puedes controlar el objetivo con las flechas del teclado para intentar evadir el misil.

## Características

-  Control interactivo del objetivo con teclado
-  Guiado de misil con algoritmo de Navegación Proporcional
-  Visualización en tiempo real de trayectorias
-  Detección de impacto
-  Restricciones físicas realistas (límites de aceleración)

## Requisitos

```bash
pip install numpy matplotlib
```

## Uso

```bash
python main.py
```

**Controles:**
- `←` Flecha izquierda: Girar a la izquierda
- `→` Flecha derecha: Girar a la derecha

## Estructura del Proyecto

```
├── main.py          # Programa principal con visualización
├── missile.py       # Clase del misil
├── target.py        # Clase del objetivo (avión)
└── pn.py           # Implementación de Navegación Proporcional
```

## Fundamentos Matemáticos

### Navegación Proporcional (PN)

La Navegación Proporcional es un algoritmo de guiado donde la aceleración lateral del misil es proporcional a la tasa de rotación de la línea de visión (Line of Sight, LOS) entre el misil y el objetivo.

#### Comando de Guiado

La aceleración normal requerida se calcula como:

```
aₙ = N · Vс · λ̇
```

Donde:
- `aₙ` = Aceleración normal (perpendicular a la velocidad del misil)
- `N` = Constante de navegación (típicamente 3-5)
- `Vс` = Velocidad de cierre (closing velocity)
- `λ̇` = Tasa de rotación de la línea de visión

#### Velocidad de Cierre

La velocidad de cierre se define como la tasa a la que disminuye la distancia entre el misil y el objetivo:

```
Vс = -(Vₜ - Vₘ) · R̂
```

Donde:
- `Vₜ` = Vector velocidad del objetivo
- `Vₘ` = Vector velocidad del misil
- `R̂` = Vector unitario de la línea de visión: `R̂ = R / |R|`
- `R` = Vector posición relativa: `R = Pₜ - Pₘ`

#### Ángulo de la Línea de Visión (LOS)

El ángulo λ se calcula como:

```
λ = arctan2(Ry, Rx)
```

Donde `Rx` y `Ry` son las componentes del vector de posición relativa.

#### Tasa de Rotación de la LOS

La tasa de rotación se aproxima numéricamente:

```
λ̇ = Δλ / Δt
```

Con normalización para evitar discontinuidades:

```
Si Δλ > π:  Δλ = Δλ - 2π
Si Δλ < -π: Δλ = Δλ + 2π
```

### Dinámica del Misil

#### Actualización del Rumbo

```
θ(t+Δt) = θ(t) + (aₙ/V) · Δt
```

Donde:
- `θ` = Ángulo de rumbo (heading)
- `V` = Velocidad del misil (constante)
- `aₙ` = Aceleración normal (limitada a ±70g)

#### Actualización de Velocidad y Posición

```
Vₓ = V · cos(θ)
Vᵧ = V · sin(θ)

x(t+Δt) = x(t) + Vₓ · Δt
y(t+Δt) = y(t) + Vᵧ · Δt
```

### Dinámica del Objetivo

El objetivo puede realizar maniobras de evasión con un límite de 9g:

```
ω_max = (g_max · g) / V
```

Donde:
- `ω_max` = Tasa máxima de giro
- `g_max` = Factor de carga máximo (9g)
- `g` = Aceleración gravitacional (9.81 m/s²)
- `V` = Velocidad del objetivo

```
θ(t+Δt) = θ(t) + ω · Δt
```

## Parámetros de Simulación

### Configuración Inicial

| Parámetro | Misil | Objetivo |
|-----------|-------|----------|
| Posición inicial | (0, 0) | (5000, 3000) m |
| Velocidad | 320 m/s | 200 m/s |
| Rumbo inicial | 45° | 30° |
| Aceleración máxima | 30g | 9g |
| Constante N | 3 | - |

### Condición de Impacto

El impacto se detecta cuando:

```
|R| = √[(xₜ - xₘ)² + (yₜ - yₘ)²] < 5 metros
```

## Interpretación Física

- **N = 3**: Guiado conservador, trayectoria suave
- **N = 4-5**: Guiado agresivo, interceptación más directa
- **Vс > 0**: El misil se acerca al objetivo
- **λ̇ > 0**: La línea de visión rota en sentido antihorario

### Ventajas de la Navegación Proporcional

1.  Implementación simple y robusta
2.  Bajo costo computacional
3.  Trayectorias predecibles y eficientes
4.  Ampliamente probado en sistemas reales

### Limitaciones

1.  Requiere medir o estimar la velocidad del objetivo
2.  Sensible a ruido en mediciones de λ
3.  Puede fallar con objetivos muy maniobrables


**¡Intenta evadir el misil!**