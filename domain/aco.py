import numpy as np


def obter_fatores_reducao_aco(theta_a: float) -> tuple[float, float, float]:
    """
    Retorna os fatores de redução ky, ke e ksig para o aço em função da temperatura.

    Parâmetros:
        theta_a: Temperatura do aço em °C.

    Retorna:
        ky: fator de redução da resistência ao escoamento
        ke: fator de redução do módulo de elasticidade
        ksig: fator de redução para tensão proporcional
    """

    if theta_a < 20:
        theta_a = 20

    if theta_a > 1200:
        theta_a = 1200

    temps = np.array([20, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200])

    ky_v = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 0.78, 0.47, 0.23, 0.11, 0.06, 0.04, 0.02, 0.0])
    ke_v = np.array([1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.31, 0.13, 0.09, 0.068, 0.045, 0.023, 0.0])
    ksig_v = np.array([1.0, 1.0, 0.89, 0.78, 0.65, 0.53, 0.30, 0.13, 0.07, 0.05, 0.03, 0.02, 0.0])

    ky = float(np.interp(theta_a, temps, ky_v))
    ke = float(np.interp(theta_a, temps, ke_v))
    ksig = float(np.interp(theta_a, temps, ksig_v))

    return ky, ke, ksig


def calcular_resistencia_compressao_fi(
    Ag: float,
    fy: float,
    E: float,
    L: float,
    K: float,
    r_min: float,
    hw_tw: float,
    bf_2tf: float,
    theta_a: float
) -> float:
    """
    Calcula a força axial resistente de cálculo em situação de incêndio.

    Retorna:
        Nfi,Rd em kN.
    """

    entradas = {
        "Ag": Ag,
        "fy": fy,
        "E": E,
        "L": L,
        "K": K,
        "r_min": r_min,
        "hw_tw": hw_tw,
        "bf_2tf": bf_2tf,
    }

    for nome, valor in entradas.items():
        if valor <= 0:
            raise ValueError(f"O parâmetro '{nome}' deve ser maior que zero.")

    if theta_a < 20:
        raise ValueError("A temperatura do aço deve ser maior ou igual a 20 °C.")

    ky, ke, ksig = obter_fatores_reducao_aco(theta_a)

    # Limites de esbeltez local
    lim_alma = 1.49 * np.sqrt(E / fy)
    lim_mesa = 0.56 * np.sqrt(E / fy)

    sujeito_local = (
        hw_tw > 0.85 * lim_alma
        or bf_2tf > 0.85 * lim_mesa
    )

    # Carga crítica de Euler
    Ne = (np.pi ** 2 * E * Ag * r_min ** 2) / ((K * L) ** 2)

    if Ne <= 0:
        raise ValueError("A carga crítica de Euler resultou inválida.")

    # Fator simplificado de redução por flambagem local
    Q = 0.947 if sujeito_local else 1.0

    lambda_0 = np.sqrt((Q * Ag * fy) / Ne)
    lambda_0_fi = lambda_0 / 0.85

    alpha = 0.022 * np.sqrt(E / fy)

    phi_0_fi = 0.5 * (
        1
        + alpha * lambda_0_fi
        + lambda_0_fi ** 2
    )

    raiz = phi_0_fi ** 2 - lambda_0_fi ** 2

    if raiz < 0:
        raise ValueError("Erro numérico no cálculo do fator de flambagem.")

    xfi = 1 / (phi_0_fi + np.sqrt(raiz))
    xfi = min(xfi, 1.0)

    if sujeito_local:
        nfi_rd = xfi * ksig * Q * Ag * fy
    else:
        nfi_rd = xfi * ky * Ag * fy

    return nfi_rd / 1000