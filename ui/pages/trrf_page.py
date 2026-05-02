import streamlit as st

from domain.trrf import (
    calcular_gamma_n,
    calcular_gamma_s1,
    calcular_tempo_equivalente,
    calcular_trrf_final,
    calcular_trrf_tabular,
    calcular_w,
)
from infra.dados_trrf import TRRF_TABELA, RISCO_ATIVACAO


def render():

    st.info(
        "A altura de incêndio deve desconsiderar barriletes, casas de máquinas, "
        "pavimentos técnicos sem permanência de pessoas e demais exceções normativas."
    )

    aba_equivalente, aba_tabular = st.tabs(
        ["Tempo Equivalente / Redutor", "Método Tabular"]
    )


    with aba_tabular:
        st.subheader("Método Tabular")

        col1, col2 = st.columns(2)

        with col1:
            ocupacao = st.selectbox(
                "Ocupação",
                list(TRRF_TABELA.keys()),
                key="ocupacao_tabular",
            )

        with col2:
            altura = st.number_input(
                "Altura de incêndio h (m)",
                min_value=0.0,
                step=0.5,
                key="altura_tabular",
            )

        try:
            trrf = calcular_trrf_tabular(ocupacao, altura)
            st.metric("TRRF tabular", f"{trrf} min")
        except ValueError:
            st.info("Preencha corretamente os dados.")

    with aba_equivalente:
        st.subheader("Método do Tempo Equivalente / Redutor")

        st.warning(
            "Este método atua como redutor do TRRF tabular. "
            "Verifique se a legislação estadual permite seu uso."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            ocupacao_eq = st.selectbox(
                "Ocupação",
                list(TRRF_TABELA.keys()),
                key="ocupacao_equivalente",
            )

            altura_incendio = st.number_input(
                "Altura de incêndio h (m)",
                min_value=0.0,
                step=0.5,
                key="altura_incendio_eq",
            )

            carga_incendio = st.number_input(
                "Carga de incêndio qfi,k (MJ/m²)",
                min_value=1.0,
                value=700.0,
                step=50.0,
            )

        with col2:
            area_piso = st.number_input(
                "Área de piso Af (m²)",
                min_value=1.0,
                value=820.0,
                step=10.0,
            )

            altura_compartimento = st.number_input(
                "Altura do compartimento H (m)",
                min_value=0.1,
                value=3.2,
                step=0.1,
            )

            area_aberturas_verticais = st.number_input(
                "Área de aberturas verticais Av (m²)",
                min_value=0.0,
                value=139.4,
                step=1.0,
            )

            area_aberturas_horizontais = st.number_input(
                "Área de aberturas horizontais Ah (m²)",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

        with col3:
            risco = st.selectbox(
                "Risco de ativação",
                list(RISCO_ATIVACAO.keys()),
                index=1,
            )

            possui_chuveiro = st.checkbox("Chuveiros automáticos")
            possui_brigada = st.checkbox("Brigada contra incêndio")
            possui_deteccao = st.checkbox("Detecção automática")

        try:
            trrf_tabular = calcular_trrf_tabular(
                ocupacao_eq,
                altura_incendio,
            )

            gamma_n = calcular_gamma_n(
                possui_chuveiro,
                possui_brigada,
                possui_deteccao,
            )

            gamma_s1 = calcular_gamma_s1(
                area_piso,
                altura_incendio,
            )

            gamma_s2 = RISCO_ATIVACAO[risco]

            w = calcular_w(
                altura_compartimento,
                area_piso,
                area_aberturas_verticais,
                area_aberturas_horizontais,
            )

            tempo_equivalente = calcular_tempo_equivalente(
                carga_incendio,
                gamma_n,
                gamma_s1,
                gamma_s2,
                w,
            )

            trrf_final = calcular_trrf_final(
                trrf_tabular,
                tempo_equivalente,
            )

            st.divider()

            c1, c2, c3 = st.columns(3)

            c1.metric("TRRF tabular", f"{trrf_tabular} min")
            c2.metric("Tempo equivalente", f"{tempo_equivalente:.1f} min")
            c3.metric("TRRF adotado", f"{trrf_final} min")

        except ValueError:
            st.info("Preencha os dados corretamente.")
