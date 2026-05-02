import numpy as np


def calcular_analise_termica_simplificada(
    tempo_total_min: float,
    fator_massividade: float,
    com_protecao: bool = False,
    dados_prot: dict | None = None,
) -> tuple[list[float], list[float]]:
    """
    Calcula a evolução simplificada da temperatura do aço em incêndio.
    """

    if tempo_total_min <= 0:
        raise ValueError("O tempo total deve ser maior que zero.")

    if fator_massividade <= 0:
        raise ValueError("O fator de massividade deve ser maior que zero.")

    if com_protecao and dados_prot is None:
        raise ValueError("Informe os dados da proteção térmica.")

    ca = 600.0
    rho_a = 7850.0
    sigma = 5.67e-8
    emis = 0.7

    dt = 5
    passos = int((tempo_total_min * 60) / dt)

    tempos_min = [0.0]
    temp_aco = [20.0]
    temp_gases = [20.0]

    for i in range(1, passos + 1):
        t_min = (i * dt) / 60
        theta_a_ant = temp_aco[-1]

        theta_g = 20 + 345 * np.log10(8 * t_min + 1)

        if not com_protecao:
            hr = sigma * emis * (
                (theta_g + 273.15) ** 4
                - (theta_a_ant + 273.15) ** 4
            )
            hc = 25 * (theta_g - theta_a_ant)
            h_total = hr + hc

            delta_theta = (
                fator_massividade / (ca * rho_a)
            ) * h_total * dt

            theta_a_novo = theta_a_ant + delta_theta

        else:
            tm = dados_prot["tm"]
            lamb_m = dados_prot["lamb_m"]
            cm = dados_prot["cm"]
            rho_m = dados_prot["rho_m"]

            if tm <= 0 or lamb_m <= 0 or cm <= 0 or rho_m <= 0:
                raise ValueError("Os dados da proteção devem ser maiores que zero.")

            phi = (rho_m * cm) / (rho_a * ca) * tm * fator_massividade

            termo_numerador = (
                fator_massividade
                * (theta_g - theta_a_ant)
                * (dt / 60)
            )

            termo_denominador = (
                (tm / lamb_m)
                * ca
                * rho_a
                * (1 + phi / 3)
            )

            termo_resfriamento = (
                (theta_g - temp_gases[-1])
                * (np.exp(phi / 10) - 1)
            )

            delta_theta = (termo_numerador / termo_denominador) - termo_resfriamento
            theta_a_novo = theta_a_ant + delta_theta

        tempos_min.append(t_min)
        temp_aco.append(theta_a_novo)
        temp_gases.append(theta_g)

    return tempos_min, temp_aco