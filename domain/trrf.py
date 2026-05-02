from infra.dados_trrf import TRRF_TABELA


def calcular_trrf_tabular(ocupacao: str, altura_incendio: float) -> int:
    if altura_incendio < 0:
        raise ValueError("A altura de incêndio não pode ser negativa.")

    dados_ocupacao = TRRF_TABELA.get(ocupacao)

    if dados_ocupacao is None:
        raise ValueError(f"Ocupação inválida: {ocupacao}")

    limites = sorted(dados_ocupacao.keys())

    for limite in limites:
        if altura_incendio <= limite:
            return dados_ocupacao[limite]

    raise ValueError("Altura acima do limite previsto na tabela.")


def calcular_gamma_n(
    possui_chuveiro: bool,
    possui_brigada: bool,
    possui_deteccao: bool,
) -> float:
    gamma_n1 = 0.60 if possui_chuveiro else 1.00
    gamma_n2 = 0.90 if possui_brigada else 1.00
    gamma_n3 = 0.90 if possui_deteccao else 1.00

    return gamma_n1 * gamma_n2 * gamma_n3


def calcular_gamma_s1(area_piso: float, altura_incendio: float) -> float:
    if area_piso <= 0:
        raise ValueError("A área de piso deve ser maior que zero.")

    gamma_s1 = 1 + (area_piso * (altura_incendio + 3)) / 100000

    return max(1.0, min(gamma_s1, 3.0))


def calcular_w(
    altura_compartimento: float,
    area_piso: float,
    area_aberturas_verticais: float,
    area_aberturas_horizontais: float,
) -> float:
    if altura_compartimento <= 0:
        raise ValueError("A altura do compartimento deve ser maior que zero.")
    if area_piso <= 0:
        raise ValueError("A área de piso deve ser maior que zero.")

    av_af = area_aberturas_verticais / area_piso
    ah_af = area_aberturas_horizontais / area_piso

    if av_af <= 0:
        raise ValueError("A relação Av/Af deve ser maior que zero.")

    termo_1 = (6 / altura_compartimento) ** 0.3

    numerador = 90 * (0.4 - av_af) ** 4
    denominador = 1 + 12.5 * (1 + 10 * av_af - av_af**2) * ah_af

    w = termo_1 * (0.62 + numerador / denominador)

    return max(w, 0.5)


def calcular_tempo_equivalente(
    carga_incendio: float,
    gamma_n: float,
    gamma_s1: float,
    gamma_s2: float,
    w: float,
) -> float:
    if carga_incendio <= 0:
        raise ValueError("A carga de incêndio deve ser maior que zero.")

    gamma_s = gamma_s1 * gamma_s2

    return 0.07 * carga_incendio * gamma_n * gamma_s * w


def calcular_trrf_final(trrf_tabular: int, tempo_equivalente: float) -> int:
    trrf_reduzido = trrf_tabular - 30

    if tempo_equivalente < trrf_reduzido:
        return max(trrf_reduzido, 15)

    if tempo_equivalente < trrf_tabular:
        return max(round(tempo_equivalente), 15)

    return trrf_tabular