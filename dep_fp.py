# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 00:39:43 2021

@author: DELL
"""

# -*- coding: utf-8 -*-

import streamlit as st   ### para reportear 
import pandas as pd      ### para leer base de datos 
import numpy as np       #### para operaciones numericas
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
   
def app() :

    ###### importamos información de los excel #################################################################################
    # PARA QUE NO DEMORE LA CARGA  BASE COMPLETA
    @st.cache(suppress_st_warning=True)
    def get_data():
        ruta ='BASE ONPE V2.xlsx'    
        base = pd.read_excel(ruta,sheet_name= "BASE", header = 0,engine ='openpyxl' )
        base["PART"] = np.round(base["N_CVAS"]/base["N_ELEC_HABIL"],3) 
        
      # ratio de participación por mes
        base["VOTO_SHARE_FP"] = base["VOTOS_P2"]/( base["VOTOS_P2"] +base["VOTOS_P1"])  # ratio de participación por mes
        base["VOTO_SHARE_PL"] = 1-base["VOTO_SHARE_FP"] 
        
        base = base[["AMBITO","DEPARTAMENTO","MESA_DE_VOTACION","VOTO_SHARE_PL","VOTO_SHARE_FP","VOTOS_P1","VOTOS_P2"]]
        return base
    
    ############################################################################################################################  
    #TITULO
    st.header('RESUMEN POR DEPARTAMENTO SEGÚN PARTIDO GANADOR') 
   
    st.write("Fuente: Oficina Nacional de Procesos Electorales (ONPE)-Datos Abiertos ")
    st.write(" https://www.datosabiertos.gob.pe/dataset/resultados-por-mesa-de-las-elecciones-presidenciales-2021-segunda-vuelta-oficina-nacional-de")
    st.write("Fecha de Descarga :2021-06-19")
    base = get_data()
    
   
    base_resumen = base[(base["AMBITO"]!="EXTRANJERO")].groupby("DEPARTAMENTO", as_index =False).agg({"MESA_DE_VOTACION":"count",
                                                                   "VOTOS_P1": "sum" , 
                                                                   "VOTOS_P2": "sum",} )
                                                                   
  
    base_resumen["share dif"] = abs(base_resumen["VOTOS_P1"]-base_resumen["VOTOS_P2"])/base_resumen["MESA_DE_VOTACION"]
  
    
    base_resumen["ESTADO"] = np.where(base_resumen["VOTOS_P1"]>base_resumen["VOTOS_P2"],
                                            "GANÓ PL", "GANÓ FP")
    
    base_resumen["VOTO_SHARE_FP"] = base_resumen["VOTOS_P2"]/( base_resumen["VOTOS_P2"] +base_resumen["VOTOS_P1"])  # ratio de participación por mes
    base_resumen["VOTO_SHARE_PL"] = 1-base_resumen["VOTO_SHARE_FP"] 
    base_resumen["VOTO_SHARE_DIFF"] = abs(base_resumen["VOTO_SHARE_PL"]-base_resumen["VOTO_SHARE_FP"])
   
    base_resumen["% MESAS"] =  base_resumen["MESA_DE_VOTACION"]/sum(base_resumen["MESA_DE_VOTACION"])
    
    base_resumen =  base_resumen[['DEPARTAMENTO', "ESTADO",
                                  "MESA_DE_VOTACION",
                                  "VOTOS_P1" , 
                                  "VOTOS_P2" ,                                 
                                  "VOTO_SHARE_PL",
                                  "VOTO_SHARE_FP",
                                  "VOTO_SHARE_DIFF",
                                  "share dif"]]
    
    base_resumen = base_resumen.rename(columns={
                                                'MESA_DE_VOTACION': 'Nro MESAS',   
                                                "VOTOS_P1": "VOTOS PL",
                                                 "VOTOS_P2": "VOTOS FP",
                                                 "VOTO_SHARE_PL": "% PL",
                                                 "VOTO_SHARE_FP": "% FP",
                                                 "VOTO_SHARE_DIFF": "DIF %",
                                                 "share dif": "Dif prom en votos"})

    base_resumen.set_index('DEPARTAMENTO', inplace=True)  
    
    def row_style(row):
        if row.Name != 'GANÓ PL':
                return pd.Series('background-color: red', row.index)
        else:
                return pd.Series('background-color: green', row.index)
    
    st.dataframe(  base_resumen.style.format({  
                                 "% PL" :" {:.2%}",
                                 "% FP" :" {:.2%}",
                                "DIF %" :" {:.2%}",
                                 "VOTOS PL":"{:,.0f}",
                                "VOTOS FP":"{:,.0f}",
                                 "Dif prom en votos":"{:,.0f}",
                                 'Nro MESAS':"{:,.0f}"
                                 }),width=1600, height=800)
     
#################################################################################################################
    st.header('DISTRIBUCIÓN DE VOTOS POR DEPARTAMENTO')
    genre = st.radio(                                   # DETERMINAR EL PARTIDO A GRAFICAR
        "Seleccione el Partido Político",
        ('Perú Libre', 'Fuerza Popular'))
    
    if genre == 'Perú Libre':
        partido = "VOTOS_P1"
        st.markdown("<h2 style='text-align: center;'>Distribución de Votos Perú Libre </h2>", unsafe_allow_html=True)
    else:
          partido = "VOTOS_P2"
          st.markdown("<h2 style='text-align: center;'>Distribución de Votos Fuerza Popular </h2>", unsafe_allow_html=True)
    
    dep2= list(base[(base["AMBITO"]=="NACIONAL")]["DEPARTAMENTO"].unique())  
    
    col1,col2,col3,col4 = st.beta_columns(4)
    
    
    fig = make_subplots(rows=9, cols=3,)
   
    for itex in range(25) :          # CREACIÓN DE CADA HISTOGRAMA
    
        globals()[f"trace{itex}"] = go.Histogram(x=base[(base["DEPARTAMENTO"]==dep2[itex])][partido], 
                                               histnorm='probability density',
                                               name = dep2[itex])
                           
    trace25 = go.Histogram(x=base[(base["AMBITO"]=="EXTRANJERO")][partido], 
                                                   histnorm='probability density',
                                                   name = "EXTRANJERO" )
                                                   
                                                     # UBICACIÓN DE CADA DEPARTAMENTO
    fig.append_trace(trace0  ,row = 1, col = 1)
    fig.append_trace(trace1  ,row = 1, col = 2)
    fig.append_trace(trace2  ,row = 1, col = 3)
    
    fig.append_trace(trace3  ,row = 2, col = 1)   
    fig.append_trace(trace4  ,row = 2, col = 2)
    fig.append_trace(trace5  ,row = 2, col = 3)
    
    fig.append_trace(trace6  ,row = 3, col = 1)
    fig.append_trace(trace7  ,row = 3, col = 2)       
    fig.append_trace(trace8  ,row = 3, col = 3)
    
    fig.append_trace(trace9  ,row = 4, col = 1)
    fig.append_trace(trace10  ,row = 4, col = 2)
    fig.append_trace(trace11  ,row = 4, col = 3)
        
    fig.append_trace(trace12  ,row = 5, col = 1)
    fig.append_trace(trace13  ,row = 5, col = 2)
    fig.append_trace(trace14  ,row = 5, col = 3)
    
    fig.append_trace(trace15  ,row = 6, col = 1)       
    fig.append_trace(trace16  ,row = 6, col = 2)
    fig.append_trace(trace17  ,row = 6, col = 3)
    
    fig.append_trace(trace18  ,row = 7, col = 1)
    fig.append_trace(trace19  ,row = 7, col = 2)   
    fig.append_trace(trace20  ,row = 7, col = 3)
    
    fig.append_trace(trace21  ,row = 8, col = 1)
    fig.append_trace(trace22  ,row = 8, col = 2)
    fig.append_trace(trace23  ,row = 8, col = 3)
        
    fig.append_trace(trace24  ,row = 9, col = 1)
    fig.append_trace(trace25  ,row = 9, col = 2)
        
    fig.update_layout(height=1800, width=1100)    # TAMAÑO DE LA FIGURA GRANDE
    st.plotly_chart(fig, use_container_width=True)
