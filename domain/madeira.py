import numpy as np

def calcular_secao_residual_madeira(t, b_mm, h_mm, tipo_madeira, lados_expostos=4):
    """
    Calcula as dimensões residuais da madeira conforme NBR 7190.
    """
    # 1. Taxa de carbonização nominal (beta_n)
    taxas = {
        "Coníferas (Serrada/MLC)": 0.70,
        "Folhosas Baixa Densidade": 0.70,
        "Folhosas Média/Alta Densidade": 0.55,
        "LVL": 0.70
    }
    beta_n = taxas.get(tipo_madeira, 0.70)

    # 2. Espessura carbonizada
    d_char_n = beta_n * t

    # 3. Espessura efetiva (e_ef) com camada adicional e0=7mm
    e0 = 7.0
    k0 = 1.0 if t >= 20 else t / 20  # Fator para tempos curtos[cite: 8]
    e_ef = d_char_n + (k0 * e0)

    # 4. Dimensões Residuais (considerando exposição)
    # Se exposto em 4 lados: retira e_ef de cada face (2 * e_ef no total)[cite: 8]
    if lados_expostos == 4:
        b_ef = max(b_mm - 2 * e_ef, 0.0)
        h_ef = max(h_mm - 2 * e_ef, 0.0)
    else:  # Ex: Viga (3 lados)
        b_ef = max(b_mm - 2 * e_ef, 0.0)
        h_ef = max(h_mm - e_ef, 0.0)

    return b_ef, h_ef, e_ef

def calcular_resistencia_madeira_fi(b_ef, h_ef, fc0k, material_tipo, L, K):
    """
    Calcula a resistência Nfi,Rd baseada no quantil de 20%[cite: 8].
    """
    if b_ef <= 0 or h_ef <= 0: return 0.0

    # 1. Propriedades para quantil de 20% (kfi * fk)[cite: 8]
    kfi_map = {
        "Madeira Serrada": 1.25,
        "Madeira Lamelada Colada": 1.15,
        "Madeira Lamelada Cruzada": 1.15,
        "LVL": 1.10
    }
    kfi = kfi_map.get(material_tipo, 1.25)

    # Resistência de cálculo em incêndio (gamma_w_fi = 1.0)[cite: 8]
    f_cd_fi = kfi * fc0k / 1.0

    # 2. Área Efetiva
    A_ef = (b_ef * h_ef) / 100  # cm²

    # 3. Verificação de Instabilidade (Simplificada para o eixo crítico)
    # No incêndio, a esbeltez aumenta pois a seção diminui[cite: 8]
    r_min = min(b_ef, h_ef) / np.sqrt(12)
    lambda_fi = (K * L) / r_min

    # Fator de redução por flambagem (kc) - Simplificado conforme slide 28[cite: 8]
    # Em uma implementação real completa, seguiria ky e lambda_rel[cite: 8]
    n_rd_fi = A_ef * f_cd_fi  # Considerando peça curta para simplificação inicial

    return n_rd_fi


