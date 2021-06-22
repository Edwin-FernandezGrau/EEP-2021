# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 08:31:20 2021

@author: EFERNANDEZ
"""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title= "Presidencial 2021")
#st.set_page_config(page_title= "Presidencial 2021",layout="wide" )

###### importamos información de los excel
ruta = 'presidencial_short.xlsx'
base = pd.read_excel(ruta,sheet_name= "BASE",header = 0,engine ='openpyxl' )



st.header('Base de Datos elección presidencial 2021 - Segunda vuelta (source : https://ronderos.pe) ')
st.dataframe(base, width=1800, height=600)


st.header('Distribución de votos por Partido (en %)')

nac_ext = list(base["v2_NACIONAL_EXTRANJERO"].unique()) 
nac_ext_SELECT = st.multiselect("Seleccione el Ámbito",nac_ext ,nac_ext )
mask_nac_ext = base["v2_NACIONAL_EXTRANJERO"].isin(nac_ext_SELECT)
base2 =  base[mask_nac_ext]


import plotly.express as px
fig01 = px.histogram(base2["v2_fp"],
                    x="v2_fp",
                    histnorm='probability density',
                    title='Dsitribución de votos por acta',
                   labels={'v2_fp':'Votos Fuerza Popular'},
                   #color_discrete_sequence=['indianred']
                   )
# Plot!
st.plotly_chart(fig01, use_container_width=True)


fig02 = px.histogram(base2["v2_perulibre"],
                    x="v2_perulibre",
                    histnorm='probability density',
                    title='Dsitribución de votos por acta',
                   labels={"v2_perulibre":'Votos Peru Libre'},
                   color_discrete_sequence=['red'], 
                   )
# Plot!
st.plotly_chart(fig02, use_container_width=True)



import plotly.figure_factory as ff

# Add histogram data
x1 = base2["v2_fp"]
x2 = base2["v2_perulibre"]

 # Group data together
hist_data = [x1, x2]
group_labels = ['Fuerza Popular', 'Peru Libre']

# Create distplot with custom bin_size
fig03 = ff.create_distplot(
         hist_data, group_labels, bin_size=[1,1],show_rug = False, colors = ["blue","red"] )

# Plot!
st.plotly_chart(fig03, use_container_width=True)



departamentos = list(base["v2_DEPARTAMENTO"].unique()) 
dep_SELECT = st.multiselect("Seleccione el Departamento",departamentos ,departamentos )
mask_nac_ext = base["v2_DEPARTAMENTO"].isin(dep_SELECT)
base2 =  base[mask_nac_ext]


# Add histogram data
x21 = base2["v2_fp"]
x22 = base2["v2_perulibre"]

 # Group data together
hist_data1 = [x21, x22]
group_labels = ['Fuerza Popular', 'Peru Libre']

# Create distplot with custom bin_size
fig04 = ff.create_distplot(
         hist_data1, group_labels, bin_size=[1,1],show_rug = False, colors = ["blue","red"] )

# Plot!
st.plotly_chart(fig04, use_container_width=True)



db_ubigeo = base.groupby(['v2_CCODI_UBIGEO'])["v2_perulibre", "v2_fp"].sum()
db_ubigeo["v2_pd_pl"] = db_ubigeo["v2_perulibre"].astype(str).str[0].astype(int)
db_ubigeo["v2_pd_fp"] = db_ubigeo["v2_fp"].astype(str).str[0].astype(int)




fig05 = px.histogram(db_ubigeo[db_ubigeo["v2_pd_pl"] != 0],
                    x="v2_pd_pl",
                    histnorm='probability density',
                    title='Dsitribución Perú Libre',
                   labels={"v2_pd_pl":'Votos Peru Libre'},
                   color_discrete_sequence=['red'],
                   )
# Plot!
st.plotly_chart(fig05, use_container_width=True)

fig06 = px.histogram(db_ubigeo[db_ubigeo["v2_pd_fp"] != 0 ],
                    x="v2_pd_fp",
                    histnorm='probability density',
                    title='Dsitribución Fuerza Popular',
                   labels={"v2_pd_fp":'Votos Fuerza Popular'},
                   color_discrete_sequence=['blue'], 
                   )
# Plot!
st.plotly_chart(fig06, use_container_width=True)



























