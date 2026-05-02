import numpy as np

def calcular_parametrica(t_min, q_fi_d, b, O_v, crescimento):
    t_h = t_min / 60.0
    mapa_t_lim = {'Lento': 25 / 60, 'Médio (20min)': 20 / 60, 'Rápido': 15 / 60}
    t_lim = mapa_t_lim[crescimento]

    # Etapa 1: Determinação do Tempo de Temperatura Máxima (t_max)[cite: 1]
    t_max_calc = 0.2e-3 * (q_fi_d / O_v)

    if t_max_calc > t_lim:
        tipo = "Ventilação"
        t_max_real = t_max_calc
        gamma = ((O_v / b) / (0.04 / 1160)) ** 2
    else:
        tipo = "Combustível"
        t_max_real = t_lim
        O_lim = 0.1e-3 * q_fi_d / t_lim
        gamma = ((O_lim / b) / (0.04 / 1160)) ** 2

    # Etapa 2: Ramo Ascendente[cite: 1]
    t_star = t_h * gamma
    temp_g = 20 + 1325 * (
                1 - 0.324 * np.exp(-0.2 * t_star) - 0.204 * np.exp(-1.7 * t_star) - 0.472 * np.exp(-19 * t_star))

    # Etapa 3: Ramo de Resfriamento[cite: 1]
    t_star_max = t_max_real * gamma
    temp_max = 20 + 1325 * (1 - 0.324 * np.exp(-0.2 * t_star_max) - 0.204 * np.exp(-1.7 * t_star_max) - 0.472 * np.exp(
        -19 * t_star_max))

    if t_max_real <= 0.5:
        taxa = 625
    elif t_max_real <= 2.0:
        taxa = 250 * (3 - t_max_real)
    else:
        taxa = 250

    temp_resf = temp_max - taxa * (t_star - t_star_max)
    return np.where(t_h <= t_max_real, temp_g, temp_resf), tipo, t_max_real * 60