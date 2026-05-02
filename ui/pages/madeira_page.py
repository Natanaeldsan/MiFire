import matplotlib.pyplot as plt
import streamlit as st

from domain.madeira import calcular_secao_residual_madeira
from domain.madeira import calcular_resistencia_madeira_fi



def render():

    c1, c2 = st.columns([1, 2])

    with c1:
        b0 = st.number_input("Largura b (mm)", value=200)
        h0 = st.number_input("Altura h (mm)", value=300)
        trrf = st.slider("TRRF (min)", 0, 120, 30)
        tipo_m = st.selectbox(
            "Material",
            ["Coníferas (Serrada/MLC)", "Folhosas Média/Alta Densidade"]
        )
        exp = st.radio("Exposição", ["4 Lados", "3 Lados"])

    with c2:
        b_ef, h_ef, e_ef = calcular_secao_residual_madeira(
            trrf,
            b0,
            h0,
            tipo_m,
            4 if "4" in exp else 3
        )

        st.subheader(f"Seção residual: {b_ef:.0f} x {h_ef:.0f} mm")
        st.metric("Espessura carbonizada (e_ef)", f"{e_ef:.1f} mm")

        fig, ax = plt.subplots()
        ax.add_patch(
            plt.Rectangle(
                (0, 0),
                b0,
                h0,
                alpha=0.3,
                label="Original"
            )
        )
        ax.add_patch(
            plt.Rectangle(
                (e_ef, e_ef),
                b_ef,
                h_ef,
                label="Residual"
            )
        )

        ax.set_xlim(-10, b0 + 10)
        ax.set_ylim(-10, h0 + 10)
        ax.set_aspect("equal")
        ax.legend()

        st.pyplot(fig)