import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from domain.curvas import (
    curva_iso834,
    curva_externa,
    curva_hidrocarboneto,
    curva_rws,
)

from domain.parametrica import calcular_parametrica


def render():
    st.markdown("### Parâmetros de Análise")

    col_entrada, col_saida = st.columns([1, 1.8])

    with col_entrada:
        opcoes = ["ISO 834", "Externa", "Hidrocarboneto", "RWS", "Paramétrica"]

        st.markdown("**Curvas de incêndio**")

        curvas = []

        col1, col2 = st.columns(2)

        for i, op in enumerate(opcoes):
            col = col1 if i % 2 == 0 else col2

            with col:
                if st.checkbox(op, value=True, key=f"curva_{op}"):
                    curvas.append(op)

        params_param = None

        if "Paramétrica" in curvas:
            st.markdown("#### Parâmetros da curva paramétrica")

            q_fi_d = st.number_input("qfi,d (MJ/m²)", value=500.0)
            b = st.number_input("Fator b", value=1160.0)
            O_v = st.number_input("Fator de ventilação Ov", value=0.04)

            crescimento = st.selectbox(
                "Crescimento do incêndio",
                ["Lento", "Médio (20min)", "Rápido"],
            )

            params_param = (q_fi_d, b, O_v, crescimento)

        tempo_max = st.slider(
            "Tempo máximo (min)",
            min_value=10,
            max_value=240,
            value=120,
            step=10,
        )

    with col_saida:
        st.markdown("### Resultado")

        if not curvas:
            st.info("Selecione pelo menos uma curva para gerar o gráfico.")
            return

        tempos = list(range(0, tempo_max + 1))

        fig, ax = plt.subplots(figsize=(9, 5))

        for curva in curvas:
            if curva == "ISO 834":
                temperaturas = [curva_iso834(t) for t in tempos]
                label = curva

            elif curva == "Externa":
                temperaturas = [curva_externa(t) for t in tempos]
                label = curva

            elif curva == "Hidrocarboneto":
                temperaturas = [curva_hidrocarboneto(t) for t in tempos]
                label = curva

            elif curva == "RWS":
                temperaturas = [curva_rws(t) for t in tempos]
                label = curva

            elif curva == "Paramétrica":
                if params_param is None:
                    continue

                q_fi_d, b, O_v, crescimento = params_param

                temperaturas, tipo, t_max = calcular_parametrica(
                    np.array(tempos),
                    q_fi_d,
                    b,
                    O_v,
                    crescimento,
                )

                label = f"Paramétrica ({tipo})"

            ax.plot(tempos, temperaturas, label=label, linewidth=2)

        ax.set_xlabel("Tempo (min)")
        ax.set_ylabel("Temperatura (°C)")
        ax.grid(True, linewidth=0.5, alpha=0.4)
        ax.legend()

        st.pyplot(fig)