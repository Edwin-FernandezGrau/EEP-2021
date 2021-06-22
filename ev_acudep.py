# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 20:19:56 2021

@author: DELL
"""


import streamlit as st   ### para reportear 
import pandas as pd      ### para leer base de datos 
import numpy as np       #### para operaciones numericas
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly
plotly.__version__

 
def app() :
      
    #TITULO
    st.title('ELECCIÓN PRESIDENCIAL 2021 - Segunda vuelta')
    st.write("Fuente: Oficina Nacional de Procesos Electorales (ONPE)-Datos Abiertos ")
    st.write(" https://www.datosabiertos.gob.pe/dataset/resultados-por-mesa-de-las-elecciones-presidenciales-2021-segunda-vuelta-oficina-nacional-de")
    st.write("Fecha de Descarga :2021-06-19")


    # PARA QUE NO DEMORE LA CARGA  BASE COMPLETA
    @st.cache(suppress_st_warning=True)
    def get_data():
        ruta ='BASE ONPE V2.xlsx'    
        base = pd.read_excel(ruta,sheet_name= "BASE", header = 0,engine ='openpyxl' )
        mask = (base["DESCRIP_ESTADO_ACTA"].isin(["CONTABILIZADA","COMPUTADA RESUELTA"]))
        base= base[mask].fillna(0)
        
        base["PART"] = np.round(base["N_CVAS"]/base["N_ELEC_HABIL"],3) 
      # ratio de participación por mes
        
        return base
    
    
    base = get_data()    



    col1,col2,col3 = st.beta_columns(3)
    dep2= list(base[(base["AMBITO"]=="NACIONAL")]["DEPARTAMENTO"].unique())

    for itex in range(25) :          # CREACIÓN DE CADA HISTOGRAMA

        mask=   (base["DEPARTAMENTO"]==dep2[itex]) 
        ave = np.sum(base[mask]["N_CVAS"])/np.sum(base[mask]["N_ELEC_HABIL"])   
        basdep = base[mask].groupby(['PART'])["VOTOS_P1","VOTOS_P2"].sum()
        
        basdep["VOTOS_VAL"]= basdep["VOTOS_P1"] + basdep["VOTOS_P2"]
        basdep['cum_PL_%'] = basdep["VOTOS_P1"].cumsum()/basdep["VOTOS_VAL"].cumsum()
        basdep['cum_FP_%'] = basdep["VOTOS_P2"].cumsum()/basdep["VOTOS_VAL"].cumsum()
        
        
        fig = go.Figure(layout_title_text=dep2[itex] )
         
        fig.add_trace(go.Scatter(x=basdep.index, y=basdep['cum_PL_%'],
                        mode='markers',
                        name='Perú Libre'))
        
        fig.add_trace(go.Scatter(x=basdep.index, y=basdep['cum_FP_%'],
                        mode='markers',
                        name='Fuerza Popular'))
    
        fig.add_vrect(x0=ave, x1=ave +0.005 ,col= 1,
                  annotation_text="average", annotation_position="top left",
                  fillcolor="green", opacity=0.25, line_width=0)
        
        fig.update_layout(showlegend=False,height=400, width=450)
        
        if (itex+1)%3 == 1 :
                col1.plotly_chart(fig, use_container_width=False)
        elif (itex+1)%3 == 2 :
                col2.plotly_chart(fig, use_container_width=False)        
        else:
                col3.plotly_chart(fig, use_container_width=False) 
   
            
            
            
 
            
            