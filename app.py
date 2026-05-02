import streamlit as st

from ui.layout import carregar_css, render_sidebar, render_topbar
from ui.pages import (
    trrf_page,
    curvas_page,
    analise_termica_page,
    aco_page,
    madeira_page,
)

st.set_page_config(
    page_title="MiFire",
    page_icon="ui/assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

carregar_css()

PAGINAS = {
    "curvas": {
        "grupo": "ANÁLISE TÉRMICA",
        "titulo": "Curvas de Incêndio",
        "descricao": "Geração e comparação de curvas temperatura-tempo.",
        "norma": "ISO 834 / Curvas parametrizadas",
        "pagina": curvas_page,
    },
    "termica": {
        "grupo": "ANÁLISE TÉRMICA",
        "titulo": "Aquecimento de Elementos",
        "descricao": "Avaliação da evolução térmica em elementos estruturais.",
        "norma": "ABNT NBR 14323",
        "pagina": analise_termica_page,
    },
    "trrf": {
        "grupo": "DIMENSIONAMENTO",
        "titulo": "TRRF",
        "descricao": "Tempo Requerido de Resistência ao Fogo.",
        "norma": "ABNT NBR 14432",
        "pagina": trrf_page,
    },
    "aco": {
        "grupo": "DIMENSIONAMENTO",
        "titulo": "Elementos de Aço",
        "descricao": "Verificação de elementos metálicos em situação de incêndio.",
        "norma": "ABNT NBR 14323",
        "pagina": aco_page,
    },
    "madeira": {
        "grupo": "DIMENSIONAMENTO",
        "titulo": "Elementos de Madeira",
        "descricao": "Cálculo da seção residual em peças de madeira.",
        "norma": "ABNT NBR 7190 / Verificações complementares",
        "pagina": madeira_page,
    },
}

if "modulo_ativo" not in st.session_state:
    st.session_state.modulo_ativo = "curvas"

render_sidebar()
pagina = PAGINAS[st.session_state.modulo_ativo]

render_topbar(pagina)

pagina["pagina"].render()