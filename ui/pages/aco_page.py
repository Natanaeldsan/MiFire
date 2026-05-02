import streamlit as st

from domain.aco import (
    obter_fatores_reducao_aco,
    calcular_resistencia_compressao_fi,
)


def render():
    temp_ref = st.session_state.get("temp_final_calculada", 500.0)

    col_entrada, col_saida = st.columns([1, 2.2])

    with col_entrada:
        st.markdown("### Dados de Entrada")

        with st.container(border=True):
            st.markdown("#### Propriedades do material e seção")

            fy = st.number_input(
                "Tensão de escoamento fy (MPa)",
                min_value=1.0,
                value=345.0,
                step=5.0,
            )

            ag = st.number_input(
                "Área bruta Ag (mm²)",
                min_value=1.0,
                value=4970.0,
                step=10.0,
            )

            r_min = st.number_input(
                "Menor raio de giração rmin (mm)",
                min_value=1.0,
                value=38.2,
                step=0.1,
            )

            comprimento = st.number_input(
                "Comprimento da barra L (mm)",
                min_value=1.0,
                value=2800.0,
                step=50.0,
            )

        with st.container(border=True):
            st.markdown("#### Condições de flambagem e temperatura")

            k_pilar = st.slider(
                "Coeficiente de flambagem K",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.05,
            )

            hw_tw = st.number_input(
                "Relação da alma h/tw",
                min_value=1.0,
                value=48.0,
                step=0.5,
            )

            bf_2tf = st.number_input(
                "Relação da mesa bf/2tf",
                min_value=1.0,
                value=8.5,
                step=0.5,
            )

            theta = st.number_input(
                "Temperatura do aço θa (°C)",
                min_value=20.0,
                max_value=1200.0,
                value=float(temp_ref),
                step=10.0,
            )

    with col_saida:
        st.markdown("### Saída de Cálculo")

        try:
            n_res = calcular_resistencia_compressao_fi(
                ag,
                fy,
                200000,
                comprimento,
                k_pilar,
                r_min,
                hw_tw,
                bf_2tf,
                theta,
            )

            ky, ke, ksig = obter_fatores_reducao_aco(theta)

            c1, c2 = st.columns(2)
            c1.metric("Nfi,Rd", f"{n_res:.2f} kN")
            c2.metric("Temperatura", f"{theta:.0f} °C")

            st.markdown("#### Fatores de redução")

            f1, f2, f3 = st.columns(3)
            f1.metric("ky", f"{ky:.3f}")
            f2.metric("ke", f"{ke:.3f}")
            f3.metric("ksig", f"{ksig:.3f}")

        except Exception as e:
            st.error(f"Erro: {e}")