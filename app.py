# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 00:39:08 2021


@author: DELL
"""

#app.py
import home
import dep_fp
import ev_acudep
import streamlit as st



PAGES = {
    "Home": home ,
    "Distribución por Departamento": dep_fp,
    "Evolución % votos acumulados ": ev_acudep
}

st.sidebar.title('Navegador')


selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]


st.sidebar.title("Acerca de ")
st.sidebar.info(
        """
        Este proyecto es mantenido por Edwin Fernández. Visiten mi twitter
        [@Ed_FernandezG](https://twitter.com/Ed_FernandezG).
"""
    )

page.app()