import streamlit as st
import matplotlib.pyplot as plt

from domain.termica_aco import calcular_analise_termica_simplificada


@st.cache_data
def executar_analise_termica(t_max, f_mass, protegido, dados_p):
    return calcular_analise_termica_simplificada(
        t_max,
        f_mass,
        protegido,
        dados_p,
    )


def render():

    col_entrada, col_saida = st.columns([1, 1.7])

    with col_entrada:
        st.markdown("### Dados de Entrada")

        with st.container(border=True):
            st.markdown("#### Elemento estrutural")

            f_mass = st.number_input(
                "Fator de massividade u/A (m⁻¹)",
                min_value=1.0,
                value=150.0,
                step=5.0,
            )

            t_max = st.slider(
                "Tempo de exposição (min)",
                min_value=10,
                max_value=120,
                value=60,
                step=5,
            )

        with st.container(border=True):
            st.markdown("#### Proteção térmica")

            protegido = st.toggle("Considerar proteção térmica", value=True)

            dados_p = None

            if protegido:
                tm = st.number_input(
                    "Espessura tm (m)",
                    min_value=0.001,
                    value=0.010,
                    step=0.001,
                    format="%.3f",
                )

                lm = st.number_input(
                    "Condutividade térmica λm (W/m°C)",
                    min_value=0.001,
                    value=0.200,
                    step=0.010,
                    format="%.3f",
                )

                cm = st.number_input(
                    "Calor específico cm (J/kg°C)",
                    min_value=1.0,
                    value=1130.0,
                    step=10.0,
                )

                rm = st.number_input(
                    "Massa específica ρm (kg/m³)",
                    min_value=1.0,
                    value=64.0,
                    step=1.0,
                )

                dados_p = {
                    "tm": tm,
                    "lamb_m": lm,
                    "cm": cm,
                    "rho_m": rm,
                }

    with col_saida:
        st.markdown("### Saída de Cálculo")

        try:
            with st.spinner("Processando análise térmica..."):
                t_plot, temp_aco = executar_analise_termica(
                    t_max,
                    f_mass,
                    protegido,
                    dados_p,
                )

            temp_final = max(temp_aco)
            st.session_state.temp_final_calculada = temp_final

            c1, c2, c3 = st.columns(3)

            c1.metric("Temperatura máxima", f"{temp_final:.1f} °C")
            c2.metric("Tempo de exposição", f"{t_max} min")
            c3.metric("u/A", f"{f_mass:.0f} m⁻¹")

            st.markdown("#### Evolução térmica")

            fig, ax = plt.subplots(figsize=(9, 5))
            ax.plot(t_plot, temp_aco, label="Temperatura do aço", linewidth=2)

            ax.set_xlabel("Tempo (min)")
            ax.set_ylabel("Temperatura (°C)")
            ax.grid(True, linewidth=0.5, alpha=0.4)
            ax.legend()

            st.pyplot(fig)

            st.markdown("#### Resumo técnico")

            if protegido:
                st.write(
                    "A análise considera proteção térmica aplicada ao elemento, "
                    "utilizando as propriedades informadas do material de proteção."
                )
            else:
                st.write(
                    "A análise considera o elemento de aço sem proteção térmica."
                )

            st.success("Análise térmica atualizada automaticamente.")

        except Exception as erro:
            st.error(f"Erro durante a análise térmica: {erro}")