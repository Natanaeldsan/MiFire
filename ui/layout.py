import os
import streamlit as st


def carregar_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles", "main.css")

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def menu_button(label, key):
    ativo = st.session_state.modulo_ativo == key

    if st.button(
        label,
        use_container_width=True,
        type="primary" if ativo else "secondary",
        key=f"menu_{key}",
    ):
        st.session_state.modulo_ativo = key
        st.rerun()


def render_sidebar():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    logo_path = os.path.join(base_dir, "ui", "assets", "logo.png")

    with st.sidebar:
        st.image(logo_path, width=60)

        menu_button("Curvas de Incêndio", "curvas")
        menu_button("Análise Térmica Simplificada", "termica")
        menu_button("TRRF", "trrf")
        menu_button("Elementos de Aço", "aco")
        menu_button("Elementos de Madeira", "madeira")

        st.caption("MiFire v1.0.0")


def render_topbar(pagina):
    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="breadcrumb">{pagina["grupo"]}</div>
            <h1>{pagina["titulo"]}</h1>
            <p>{pagina["descricao"]}</p>
        </div>
        <div class="standard-box">
            <span>Referência normativa</span>
            <strong>{pagina["norma"]}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)