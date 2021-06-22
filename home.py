# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 20:21:46 2021

@author: DELL
"""
import streamlit as st   ### para reportear 
import pandas as pd      ### para leer base de datos 
import numpy as np       #### para operaciones numericas
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(page_title= "Presidencial 2021", layout="wide")

 
def app() :
      
    #TITULO
    st.title('ELECCIÓN PRESIDENCIAL 2021 - Segunda vuelta')
    st.write("Fuente: Oficina Nacional de Procesos Electorales (ONPE)-Datos Abiertos ")
    st.write(" https://www.datosabiertos.gob.pe/dataset/resultados-por-mesa-de-las-elecciones-presidenciales-2021-segunda-vuelta-oficina-nacional-de")
    st.write("Fecha de Descarga :2021-06-19")
    
    # "VOTOS_P1" = PERU LIBRE
    # "VOTOS_P2" = FUERZA POPULAR
        
    ###### importamos información de los excel #################################################################################
    # PARA QUE NO DEMORE LA CARGA  BASE COMPLETA
    @st.cache(suppress_st_warning=True)
    def get_data():
        ruta ='BASE ONPE V2.xlsx'    
        base = pd.read_excel(ruta,sheet_name= "BASE", header = 0,engine ='openpyxl' )
        mask = (base["DESCRIP_ESTADO_ACTA"].isin(["CONTABILIZADA","COMPUTADA RESUELTA"]))
        base= base[mask].fillna(0)
        
        base["PART"] = np.round(base["N_CVAS"]/base["N_ELEC_HABIL"],3) 
      # ratio de participación por mes
        base["VOTO_SHARE_FP"] = base["VOTOS_P2"]/( base["VOTOS_P2"] +base["VOTOS_P1"])  # ratio de participación por mes
        base["VOTO_SHARE_PL"] = base["VOTOS_P1"]/( base["VOTOS_P2"] +base["VOTOS_P1"])
        base["VOTO_PL_FP"] =base["VOTOS_P2"]/( base["VOTOS_P2"] +base["VOTOS_P1"])
        base["VOTO_SHARE_DIFF"] = abs(base["VOTO_SHARE_PL"]-base["VOTO_SHARE_FP"])
        
        
        base["NO_VOT"] = base["N_ELEC_HABIL"] - base["N_CVAS"] 
        base["v2_ud_pl"] = base["VOTOS_P1"].fillna(0).astype(str).str[-3].astype(int)
        base["v2_ud_fp"] = base["VOTOS_P2"].fillna(0).astype(str).str[-3].astype(int)
        base["v2_ud_nul"] = base["VOTOS_VN"].fillna(0).astype(str).str[-3].astype(int)
        base["v2_ud_vb"] = base["VOTOS_VB"].fillna(0).astype(str).str[-3].astype(int)
        base["v2_ud_cvas"] = base["N_CVAS"].fillna(0).astype(str).str[-3].astype(int)
        base["v2_ud_nvot"] = base["NO_VOT"].fillna(0).astype(str).str[-3].astype(int)
        
        
        base["estado_fp"] = np.where(base["VOTO_SHARE_FP"]>0.5,
                                            "GANÓ FP", "NO GANÓ FP")
        
        base["estado_pl"] = np.where(base["VOTO_SHARE_PL"]>0.5,
                                            "GANÓ PL", "NO GANÓ PL")
        
        base["estado_f"] = np.where(base["VOTO_SHARE_PL"]>0.5,
                                            "GANÓ PL", "GANÓ FP")
        base["estado_f"] = np.where(base["VOTO_SHARE_PL"]==0.50000,
                                            "IGUALES", base["estado_f"])
        
        base["va_pl"] = base["VOTOS_P1"] - base["VOTOS_P2"] 
        base["va_fp"] = base["VOTOS_P2"] - base["VOTOS_P1"] 
        return base
    
    
    base = get_data()    
       
    @st.cache
    def get_data1():
    
        db_ubigeo = base.groupby(['UBIGEO'])["VOTOS_P1","VOTOS_P2","VOTOS_VB","VOTOS_VN","N_CVAS","N_ELEC_HABIL"].sum()
        db_ubigeo["NO_VOT"] = db_ubigeo["N_ELEC_HABIL"] - db_ubigeo["N_CVAS"] 
        
        
        # primer digito
        db_ubigeo["v2_pd_pl"] = db_ubigeo["VOTOS_P1"].astype(str).str[0].astype(int)
        db_ubigeo["v2_pd_fp"] = db_ubigeo["VOTOS_P2"].astype(str).str[0].astype(int)
        
        
        # ultimo dígito
        db_ubigeo["v2_ud_pl"] = db_ubigeo["VOTOS_P1"].astype(str).str[-3].astype(int)
        db_ubigeo["v2_ud_fp"] = db_ubigeo["VOTOS_P2"].astype(str).str[-3].astype(int)
        db_ubigeo["v2_ud_nul"] = db_ubigeo["VOTOS_VN"].astype(str).str[-3].astype(int)
        db_ubigeo["v2_ud_vb"] = db_ubigeo["VOTOS_VB"].astype(str).str[-3].astype(int)
        db_ubigeo["v2_ud_cvas"] = db_ubigeo["N_CVAS"].astype(str).str[-3].astype(int)
        db_ubigeo["v2_ud_nvot"] = db_ubigeo["NO_VOT"].astype(str).str[-3].astype(int)

        return  db_ubigeo

    db_ubigeo = get_data1()

 
      ######################################      1     #########################################################################
    
    st.header('1. DISTRIBUCIÓN DE ACTAS')
    st.subheader('1.1 Distribución porcentual del número de actas por cantidad de votos obtenidos')
    col1,col2 = st.beta_columns(2)
    
    altura=350
    ancho=450
    
                                        # DISTRIBUCION DE VOTOS PERU LIBRE
    fig01 = px.histogram(base,
                         x="VOTOS_P1",
                        histnorm='probability density',
                        #title='Distribución de votos por acta',
                        labels={"VOTOS_P1":'Votos Peru Libre'},
                        #color_discrete_sequence= ['orangered']# ,facet_col="DEPARTAMENTO"
                        )
    
    ################################
                                        # DISTRIBUCION DE VOTOS FUERZA POPULAR
    fig02 = px.histogram(base["VOTOS_P2"],
                         x="VOTOS_P2",
                         histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"VOTOS_P2":'Votos Fuerza Popular'},
                         color_discrete_sequence= ['orangered']
                       )
    
    
    fig01.update_layout(height=altura, width=ancho)
    fig02.update_layout(height=altura, width=ancho)
    
    col1.plotly_chart(fig01, use_container_width=True)
    col2.plotly_chart(fig02, use_container_width=True)
    
    
    ################################   AMBOS
    col1,col2,col3 = st.beta_columns([1,2,1])
    

    
    # Add histogram data
    x1 = base["VOTOS_P2"].fillna(0)
    x2 = base["VOTOS_P1"].fillna(0)
    
     # Group data together
    hist_data = [x1, x2]
    group_labels = ['Fuerza Popular', 'Peru Libre']
    
    # Create distplot with custom bin_size
    fig03 = ff.create_distplot(
             hist_data,
             group_labels,
             bin_size=[1,1],
             show_rug = False,
             colors = ["red","blue"]
             )
   
    
    fig03.update_layout(height=altura+75, width=ancho+100)
    col2.plotly_chart(fig03, use_container_width=True)
    
    ###################################  1.2   ###############################################################
    
    st.subheader('1.2 Distribución porcentual del número de actas por porcentaje de votos obtenidos')
    
     ########################                                      # VOTO COMPARTIDO PERU LIBRE
    col1,col2 = st.beta_columns(2)
    fig01 = px.histogram(base["VOTO_SHARE_PL"],
                         x="VOTO_SHARE_PL",
                        histnorm='probability density',
                        #title='Distribución de votos por acta',
                        labels={"VOTO_SHARE_PL":' % Votos Peru Libre'},
                        #color_discrete_sequence= ['orangered']# ,facet_col="DEPARTAMENTO"
                        )
    
    
      ##############                                      # VOTO COMPARTIDO PERU LIBRE
    fig02 = px.histogram(base["VOTO_SHARE_FP"],
                         x="VOTO_SHARE_FP",
                         histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"VOTO_SHARE_FP":' % Votos Fuerza Popular'},
                         color_discrete_sequence= ['orangered']
                       )
   
    fig01.update_layout(height=altura, width=ancho)
    fig02.update_layout(height=altura, width=ancho)
    
    col1.plotly_chart(fig01, use_container_width=True)
    col2.plotly_chart(fig02, use_container_width=True)
    
    
    
    ####################################     1.3     ################################################################
    st.subheader('1.3 Distribución  de actas por número de votos obtenidos, según se ganó o no en esa acta')
    
      ###############                                      # FUERZA POPULAR GANA
    col1,col2,col3 = st.beta_columns(3)
    
  
    col1.markdown("<h5 style='text-align: center;'>Distribución de actas donde ganó FP, por número de votos</h5>", unsafe_allow_html=True)

    mask=   ( base["estado_fp"]== "GANÓ FP") 
    fig01 = px.histogram(base[mask]["VOTOS_P2"],
                         x="VOTOS_P2",
                         #histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"VOTOS_P2":'  Votos Fuerza Popular'},
                         color_discrete_sequence= ['orangered']
                       )
    
      ##################                                  # FUERZA POPULAR NO GANA
    
    col2.markdown("<h5 style='text-align: center;'>Distribución de actas donde no ganó FP, por número de votos</h5>", unsafe_allow_html=True)
    mask=   ( base["estado_fp"]== "NO GANÓ FP") 
    fig02 = px.histogram(base[mask]["VOTOS_P2"],
                         x="VOTOS_P2",
                         #histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"VOTOS_P2":'  Votos Fuerza Popular'},
                         color_discrete_sequence= ['#7F7F7F']
                       )

    ###########################                                 AMBOS
  
    col3.markdown("<h5 style='text-align: center;'>Distribución de actas por número de votos</h5>", unsafe_allow_html=True)     
    fig03 = px.histogram(base,
                         x="VOTOS_P2",
                         color = "estado_fp",
                         #histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"VOTOS_P2":'  Votos Fuerza Popular'},
                         color_discrete_sequence= ['#7F7F7F','orangered']
                       )
    
    
    
    
    
    # fig.update_layout(
    #     title_text='Sampled Results', # title of plot
    #     xaxis_title_text='Value', # xaxis label
    #     yaxis_title_text='Count', # yaxis label
    #     bargap=0.2, # gap between bars of adjacent location coordinates
    #     bargroupgap=0.1 # gap between bars of the same location coordinates
    # )
    
   
    fig01.update_layout(height=altura, width=ancho-5 )
    fig02.update_layout(height=altura, width=ancho-5)
    fig03.update_layout(height=altura, width=ancho+5)
    
    col1.plotly_chart(fig01, use_container_width=True)
    col2.plotly_chart(fig02, use_container_width=True)
    col3.plotly_chart(fig03, use_container_width=True)
    
    
    
    
    #########################    # GANO PL
    
    col1.markdown("<h5 style='text-align: center;'>Distribución de actas donde ganó PL, por número de votos</h5>", unsafe_allow_html=True)
   
    
    mask=   ( base["estado_pl"]== "GANÓ PL") 
    fig01 = px.histogram(base[mask]["VOTOS_P1"],
                         x="VOTOS_P1",
                         #histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"VOTOS_P1":'  Votos Perú Libre'},
                         #color_discrete_sequence= ['orangered']
                       )
    
    #########################    # NO  GANO PL
    col2.markdown("<h5 style='text-align: center;'>Distribución de actas donde no ganó PL, por número de votos</h5>", unsafe_allow_html=True)
   
    
    
    mask=   ( base["estado_pl"]== "NO GANÓ PL") 
    fig02 = px.histogram(base[mask]["VOTOS_P1"],
                         x="VOTOS_P1",
                         #histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"VOTOS_P1":'  Votos Perú Libre'},
                         color_discrete_sequence= ['#7F7F7F']
                       )
  
    
    #########################    # AMBOS
    col3.markdown("<h5 style='text-align: center;'>Distribución de actas por número de votos</h5>", unsafe_allow_html=True)
  
          
    fig03 = px.histogram(base,
                         x="VOTOS_P1",
                         color = "estado_pl",
                         #histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"VOTOS_P1":'  Votos Perú Libre'},
                         color_discrete_sequence= ['#676EFA','#7F7F7F']
                       )
    
    fig01.update_layout(height=altura, width=ancho-5)
    fig02.update_layout(height=altura, width=ancho-5)
    fig03.update_layout(height=altura, width=ancho+5)
    
    col1.plotly_chart(fig01, use_container_width=True)
    col2.plotly_chart(fig02, use_container_width=True)
    col3.plotly_chart(fig03, use_container_width=True)
    
    
    ################################## 4      ##############################################################################
    # st.subheader('1.5 Distribución  de actas por porcentaje de votos obtenidos, según se ganó o no en esa acta')
    #  ##############                                       # FUERZA POPULAR GANA
    # col1,col2,col3 = st.beta_columns(3)
    
    # col1.subheader('Distribución de actas donde ganó FP por % de votos')
    
    # mask=   ( base["estado_fp"]== "GANÓ FP") 
    # fig01 = px.histogram(base[mask]["VOTO_SHARE_FP"],
    #                      x="VOTO_SHARE_FP",
    #                      #histnorm='probability density',
    #                     # title='Dsitribución de votos por acta',
    #                      #labels={"VOTO_SHARE_FP":' % Votos Fuerza Popular'},
    #                      color_discrete_sequence= ['orangered']
    #                    )
    
    #  #################                                   # FUERZA POPULAR NO GANA
    # col2.subheader('Distribución de actas donde no ganó FP por % de votos')
    
    # mask=   ( base["estado_fp"]== "NO GANÓ FP") 
    # fig02 = px.histogram(base[mask]["VOTO_SHARE_FP"],
    #                      x="VOTO_SHARE_FP",
    #                      #histnorm='probability density',
    #                     # title='Dsitribución de votos por acta',
    #                      #labels={"VOTO_SHARE_FP":' % Votos Fuerza Popular'},
    #                      color_discrete_sequence= ['#7F7F7F']
    #                    )
    # # Plot!
    # #st.plotly_chart(fig01, use_container_width=True)
    # ##################################          AMBOS
    # col3.subheader('Distribución de actas por % de votos')
          
    # fig03 = px.histogram(base,
    #                      x="VOTO_SHARE_FP",
    #                      color = "estado_fp",
    #                      #histnorm='probability density',
    #                     # title='Dsitribución de votos por acta',
    #                      #labels={"VOTO_SHARE_FP":' % Votos Fuerza Popular'},
    #                      color_discrete_sequence= ['#7F7F7F','orangered']
    #                    )
    
    
    # # fig.update_layout(
    # #     title_text='Sampled Results', # title of plot
    # #     xaxis_title_text='Value', # xaxis label
    # #     yaxis_title_text='Count', # yaxis label
    # #     bargap=0.2, # gap between bars of adjacent location coordinates
    # #     bargroupgap=0.1 # gap between bars of the same location coordinates
    # # )
                                  
    
    # # Plot!
    # #st.plotly_chart(fig02, use_container_width=True)
    # fig01.update_layout(height=altura, width=ancho-5)
    # fig02.update_layout(height=altura, width=ancho-5)
    # fig03.update_layout(height=altura+20, width=ancho+5)
    
    # col1.plotly_chart(fig01, use_container_width=False)
    # col2.plotly_chart(fig02, use_container_width=False)
    # col3.plotly_chart(fig03, use_container_width=False)
    
    
    # ########################### GANO PL
    
    # col1.subheader('Distribución de actas donde ganó PL por % de votos')
    
    # mask=   ( base["estado_pl"]== "GANÓ PL") 
    # fig01 = px.histogram(base[mask]["VOTO_SHARE_PL"],
    #                      x="VOTO_SHARE_PL",
    #                      #histnorm='probability density',
    #                     # title='Dsitribución de votos por acta',
    #                      #labels={"VOTO_SHARE_FP":' % Votos Fuerza Popular'},
    #                      #color_discrete_sequence= ['orangered']
    #                    )
    
    # ########################### NO  GANO PL
    # col2.subheader('Distribución de actas donde no ganó PL por % de votos')
    
    
    # mask=   ( base["estado_pl"]== "NO GANÓ PL") 
    # fig02 = px.histogram(base[mask]["VOTO_SHARE_PL"],
    #                      x="VOTO_SHARE_PL",
    #                      #histnorm='probability density',
    #                     # title='Dsitribución de votos por acta',
    #                      #labels={"VOTO_SHARE_FP":' % Votos Fuerza Popular'},
    #                      color_discrete_sequence= ['#7F7F7F']
    #                    )
    # # Plot!
    # #st.plotly_chart(fig01, use_container_width=True)
    
    # ###########################  AMBOS
    # col3.subheader('Distribución de actas por % de votos')
          
    # fig03 = px.histogram(base,
    #                      x="VOTO_SHARE_PL",
    #                      color = "estado_pl",
    #                      #histnorm='probability density',
    #                     # title='Dsitribución de votos por acta',
    #                      #labels={"VOTO_SHARE_FP":' % Votos Fuerza Popular'},
    #                      color_discrete_sequence= ['#676EFA','#7F7F7F']
    #                    )
    
                                            
    # # Plot!
    # #st.plotly_chart(fig02, use_container_width=True)
    # fig01.update_layout(height=altura, width=ancho-5)
    # fig02.update_layout(height=altura, width=ancho-5)
    # fig03.update_layout(height=altura+20, width=ancho+5)
    
    # col1.plotly_chart(fig01, use_container_width=False)
    # col2.plotly_chart(fig02, use_container_width=False)
    # col3.plotly_chart(fig03, use_container_width=False)
    
    ############################################ 5 #############################################################
    #col1 = st.beta_columns(1)
    
    st.subheader('1.4 Distribución  de actas ganadas por diferencia de votos a favor')
    
    col1,col2,col3 = st.beta_columns(3)
    col1.markdown("<h5 style='text-align: center;'>Distribución de actas por nro de votos a favor - PL</h5>", unsafe_allow_html=True) 
    
    mask=   ( base["estado_pl"]== "GANÓ PL") 
    fig01 = px.histogram(base[mask]["va_pl"],
                         x="va_pl",
                         histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"va_pl":' Dif votos a favor PL'},
                         #color_discrete_sequence= ['orangered']
                       )
    col2.markdown("<h5 style='text-align: center;'>Distribución de actas por nro de votos a favor - FP</h5>", unsafe_allow_html=True) 
    #col2.subheader('Distribución de actas por nro de votos a favor - FP')
    mask=   ( base["estado_fp"]== "GANÓ FP") 
    fig02 = px.histogram(base[mask]["va_fp"],
                         x="va_fp",
                         histnorm='probability density',
                        # title='Dsitribución de votos por acta',
                         labels={"va_fp":' Dif votos a favor FP'},
                         color_discrete_sequence= ['orangered']
                       )
    
    
    fig01.update_layout(height=altura, width=ancho-5)
    fig02.update_layout(height=altura, width=ancho-5)
    #"fig03.update_layout(height=altura+20, width=ancho+5)
    
    col1.plotly_chart(fig01, use_container_width=True)
    col2.plotly_chart(fig02, use_container_width=True)
    #"col3.plotly_chart(fig03, use_container_width=False)
    
    
    
    
    ############################################ 5 .1 #############################################################
    col1= st.beta_columns(1)
    st.subheader('1.5 Distribución acumulada de actas ganadas por diferencia de votos a favor')
    col1,col2,col3 = st.beta_columns(3)
     
    col1.markdown("<h5 style='text-align: center;'>Distribución acumulada de actas por nro de votos a favor - PL</h5>", unsafe_allow_html=True)
    #col1.subheader('Distribución acumulada de actas por nro de votos a favor - PL')
    
    mask=   ( base["estado_pl"]== "GANÓ PL") 
    fig01 = px.histogram(base[mask]["va_pl"],
                         x="va_pl",
                         histnorm='probability density',
                         cumulative = True,
                        # title='Dsitribución de votos por acta',
                         labels={"va_pl":' Dif votos a favor PL'},
                         #color_discrete_sequence= ['orangered']
                       )
    
    col2.markdown("<h5 style='text-align: center;'>Distribución acumulada de actas por nro de votos a favor - FP</h5>", unsafe_allow_html=True)
    #col2.subheader('Distribución acumulada de actas por nro de votos a favor - FP')
    mask=   ( base["estado_fp"]== "GANÓ FP") 
    fig02 = px.histogram(base[mask]["va_fp"],
                         x="va_fp",
                         histnorm='probability density',
                         cumulative = True,
                        # title='Dsitribución de votos por acta',
                          labels={"va_fp":' Dif votos a favor PL'},
                         color_discrete_sequence= ['orangered']
                       )
    
    
    fig01.update_layout(height=altura, width=ancho-5)
    fig02.update_layout(height=altura, width=ancho-5)
    #"fig03.update_layout(height=altura+20, width=ancho+5)
    
    col1.plotly_chart(fig01, use_container_width=True)
    col2.plotly_chart(fig02, use_container_width=True)
    #"col3.plotly_chart(fig03, use_container_width=False)
    
    
    ############################################ 5 .2   #############################################################
     # DISTRIBUCÓN DE NRO DE ACTAS SEGUN DE LA FIECNCIA DE VOTOS NE LA MESAS QUE GANARON
     
    col1.markdown("<h5 style='text-align: center;'>Distribución acumulada de actas ganadas por  % de votos - PL</h5>", unsafe_allow_html=True) 
    #col1.subheader('Distribución acumulada de actas ganadas por  % de votos - PL')
    
    mask=   ( base["estado_pl"]== "GANÓ PL") 
    fig01 = px.histogram(base[mask]["VOTO_SHARE_PL"],
                         x="VOTO_SHARE_PL",
                         histnorm='probability density',
                         cumulative = True,
                        # title='Dsitribución de votos por acta',
                         labels={"VOTO_SHARE_PL":' % Votos Perú Libre'},
                         #color_discrete_sequence= ['orangered']
                       )
    col2.markdown("<h5 style='text-align: center;'>Distribución acumulada de actas ganadas por % de votos - FP</h5>", unsafe_allow_html=True) 
    #col2.subheader('Distribución acumulada de actas ganadas por % de votos - FP')
    mask=   ( base["estado_fp"]== "GANÓ FP") 
    fig02 = px.histogram(base[mask]["VOTO_SHARE_FP"],
                         x="VOTO_SHARE_FP",
                         histnorm='probability density',
                         cumulative = True,
                        # title='Dsitribución de votos por acta',
                         labels={"VOTO_SHARE_FP":' % Votos Fuerza Popular'},
                         color_discrete_sequence= ['orangered']
                       )
    
    
    fig01.update_layout(height=altura, width=ancho-5)
    fig02.update_layout(height=altura, width=ancho-5)
    #"fig03.update_layout(height=altura+20, width=ancho+5)
    
    col1.plotly_chart(fig01, use_container_width=True)
    col2.plotly_chart(fig02, use_container_width=True)
    #"col3.plotly_chart(fig03, use_container_width=False)
    
   #####################################################################################
   
   
    st.subheader('1.6. Resumen por mesa según partido político ganador') 
     
    #b222 = base.pivot_table(index = "estado_f", values = ["MESA_DE_VOTACION","VOTOS_P1","VOTOS_P2"], aggfunc = ["count","sum"]) 
    base_resumen = base.groupby("estado_f", as_index =False).agg({"MESA_DE_VOTACION":"count",
                                                                   "VOTOS_P1": "sum" , 
                                                                   "VOTOS_P2": "sum",
                                                                   "VOTO_SHARE_FP": "mean",
                                                                   "VOTO_SHARE_PL": "mean",
                                                                   "VOTO_SHARE_DIFF": "mean"})
    
    
    base_resumen["share dif"] = abs(base_resumen["VOTOS_P1"]-base_resumen["VOTOS_P2"])/base_resumen["MESA_DE_VOTACION"]
  
    # base_resumen.style.format("{:.2%}")
    
    # base_resumen.style.format({  "VOTO_SHARE_FP" :" {:.2%}",
    #                             "VOTO_SHARE_PL" :" {:.2%}",
    #                             "VOTO_SHARE_DIFF" :" {:.2%}"
    #                            })
    
    
    base_resumen["% MESAS"] =  base_resumen["MESA_DE_VOTACION"]/sum(base_resumen["MESA_DE_VOTACION"])
    
    base_resumen =  base_resumen[['estado_f',
                                  "MESA_DE_VOTACION",
                                  "% MESAS",
                                  "VOTOS_P1" , 
                                  "VOTOS_P2" ,
                                  "VOTO_SHARE_PL",
                                  "VOTO_SHARE_FP",                              
                                  "VOTO_SHARE_DIFF",
                                  "share dif"]]
    
    base_resumen = base_resumen.rename(columns={'estado_f': 'ESTADO MESAS', 
                                                'MESA_DE_VOTACION': 'Nro MESAS',
                                                "% MESAS":"% MESAS",
                                                "VOTOS_P1": "VOTOS PL",
                                                 "VOTOS_P2": "VOTOS FP",
                                                 "VOTO_SHARE_PL": "% PL",
                                                 "VOTO_SHARE_FP": "% FP",
                                                 "VOTO_SHARE_DIFF": "DIF %",
                                                 "share dif": "Dif prom en votos"
                                                })
    
       
    st.dataframe(  base_resumen.style.format({  "% MESAS" :" {:.2%}",
                                "% PL" :" {:.2%}",
                                "% FP" :" {:.2%}",
                                "DIF %" :" {:.2%}",
                                "VOTOS PL":"{:,.0f}",
                                "VOTOS FP":"{:,.0f}",
                                "Dif prom en votos":"{:,.0f}",
                                'Nro MESAS':"{:,.0f}"
                                }))
    
   # st.write( " Fuerza Popular ganó en el 57.04% de mesas,obteniendo una diferencia promedio de 63 votos por mesa.  \n En tanto, Perú ganó en menos mesas (42.51%) pero obtuvo una diferencia promedio mayor (86 votos por mesa).")
    st.markdown("<h5 style='text-align: center;'>Fuerza Popular ganó en el 57.04% de mesas,obteniendo una diferencia promedio de 63 votos por mesa.  \n En tanto, Perú ganó en menos mesas (42.51%) pero obtuvo una diferencia promedio mayor (86 votos por mesa).</h5>", unsafe_allow_html=True)    
   
   
   
   
   
    
    #################################################
    st.header('2. DISTRIBUCIÓN DEL PRIMER DÍGITO DE LOS VOTOS POR DISTRITO') 
    #GRAFICAMOS LEY DE BENFORD
    
    
    
    fig = make_subplots(rows=1, cols=2 )
    d2 = go.Histogram(x=db_ubigeo[db_ubigeo["v2_pd_pl"] != 0]["v2_pd_pl"], 
                                               histnorm='probability density',
                                               name = "PERU LIBRE", 
                                               )
    d1 = go.Histogram(x=db_ubigeo[db_ubigeo["v2_pd_fp"] != 0]["v2_pd_fp"], 
                                               histnorm='probability density',
                                               name = "FUERZA POPULAR",
                                               )
    
    
    
    fig.append_trace(d2  ,row = 1, col = 1)
    fig.append_trace(d1  ,row = 1, col = 2)
    
    fig.update_layout(height=450, width=900, bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    #####################################################################################################
    
    tamaño = True
    st.header('3. DISTRIBUCIÓN DEL ULTIMO DÍGITO DE LOS VOTOS POR DISTRITO') 
    
    
    #FORMATO DE 3 COLUMNAS
    col1,col2,col3 = st.beta_columns(3) 
    width=450
    height=350 
    
     ##############                       # PERU LIBRE
    x ="v2_ud_pl"
    title = "Perú Libre"
    fig = px.histogram(db_ubigeo, x= x, #y="total_bill", #color="sex",
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                       width=width, height=height   ) 
    
    
    fig.add_shape( type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    fig.update_layout(bargap=0.2)
    col1.plotly_chart(fig, use_container_width=tamaño)
    
    
     ###############                   # FUERZA POPULAR
    x ="v2_ud_fp"
    title = "Fuerza Popular"
    fig = px.histogram(db_ubigeo, x= x, #y="total_bill", #color="sex",
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                      width=width, height=height,
                       color_discrete_sequence=['orangered'] 
                           )
    
    fig.add_shape( # add a horizontal "target" line
         type="line",  line_color="grey", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    fig.update_layout(bargap=0.2)
    col2.plotly_chart(fig, use_container_width=tamaño)
    
    
    
       #################                 # VOTOS NULOS
    x ="v2_ud_nul"
    title = "Votos nulos"
    fig = px.histogram(db_ubigeo, x= x,
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                       color_discrete_sequence=['#7F7F7F'] ,
                       width=width, height=height  )
    
    fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
         x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    
    
    fig.update_layout(bargap=0.2)
    col3.plotly_chart(fig, use_container_width=tamaño)
    
     ##########                   # VOTOS EN BLANCO
    # x ="v2_ud_vb"
    # title = "Votos en blanco"
    # fig = px.histogram(db_ubigeo, x= x,
    #                    histnorm='probability density',
    #                    title=title, 
    #                    labels={x:"Último dígito"},
    #                    color_discrete_sequence=['#AB63FA'] ,
    #                   width=width, height=height )
    
    # fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    #      x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    # fig.update_layout(bargap=0.2)
    # col1.plotly_chart(fig, use_container_width=False)
    
       #############                 # VOTOS TOTALES
    x ="v2_ud_cvas"
    title = "Total Votantes"
    fig = px.histogram(db_ubigeo, x= x,
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                       width=width, height=height,
                       color_discrete_sequence=['#7F7F7F'])
    
    fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
         x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    fig.update_layout(bargap=0.2)
    col1.plotly_chart(fig, use_container_width=tamaño)
    
    
    ##############                 # VOTOS NO FUERON
    x ="v2_ud_cvas"
    title = "No votaron"
    fig = px.histogram(db_ubigeo, x= x,
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                       width=width, height=height,
                       color_discrete_sequence=['#7F7F7F'])
    
    fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
         x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    fig.update_layout(bargap=0.2)
    col2.plotly_chart(fig, use_container_width=tamaño)
    
    
    

        
        
    col1 = st.beta_columns(1) 
    st.header('3. DISTRIBUCIÓN DE ULTIMO DÍGITO EN LOS VOTOS POR MESA') 
    
    # fig = px.histogram(base2, x="v2_ud_pl", #y="total_bill", #color="sex",
    #                    histnorm='probability density',
    #            # title="DISTRIBUCIÓN DE LOS PRIMEROS DÍGITOS",
    #             width=600, height=400,
    #            # template="simple_white"
    #             )
    
    # fig.add_shape( # add a horizontal "target" line
    #     type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    #     x0=0, x1=1, xref="paper", y0=0.10, y1=0.10, yref="y"
    # )
    
    # fig.update_layout(bargap=0.2)
    # col1.plotly_chart(fig, use_container_width=False)
    
    
    
    col1,col2,col3 = st.beta_columns(3) 
     #############                       # PERU LIBRE
    x ="v2_ud_pl"
    title = "Perú Libre"
    fig = px.histogram(base, x= x, #y="total_bill", #color="sex",
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                       width=width, height=height   ) 
    
    
    fig.add_shape( type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    fig.update_layout(bargap=0.2)
    col1.plotly_chart(fig, use_container_width=tamaño)
    
    
        ###############                # FUERZA POPULAR
    x ="v2_ud_fp"
    title = "Fuerza Popular"
    fig = px.histogram(base, x= x, #y="total_bill", #color="sex",
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                      width=width, height=height,
                       color_discrete_sequence=['orangered'] 
                           )
    
    fig.add_shape( # add a horizontal "target" line
         type="line",  line_color="grey", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    fig.update_layout(bargap=0.2)
    col2.plotly_chart(fig, use_container_width=tamaño)
    
    
    
     ###############                   # VOTOS NULOS
    x ="v2_ud_nul"
    title = "Votos nulos"
    fig = px.histogram(base, x= x,
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                       color_discrete_sequence=['#7F7F7F'] ,
                       width=width, height=height  )
    
    fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
         x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    
    
    fig.update_layout(bargap=0.2)
    col3.plotly_chart(fig, use_container_width=tamaño)
    
    #                     # VOTOS EN BLANCO
    # x ="v2_ud_vb"
    # title = "Votos en blanco"
    # fig = px.histogram(base2, x= x,
    #                    histnorm='probability density',
    #                    title=title, 
    #                    labels={x:"Último dígito"},
    #                    color_discrete_sequence=['#AB63FA'] ,
    #                   width=width, height=height )
    
    # fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    #      x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    # fig.update_layout(bargap=0.2)
    # col1.plotly_chart(fig, use_container_width=False)
    
        #################                # VOTOS TOTALES
    x ="v2_ud_cvas"
    title = "Total Votantes"
    fig = px.histogram(base, x= x,
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                       width=width, height=height,
                       color_discrete_sequence=['#7F7F7F'])
    
    fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
         x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    fig.update_layout(bargap=0.2)
    col1.plotly_chart(fig, use_container_width=tamaño)
    
    
        ###########              # VOTOS NO FUERON
    x ="v2_ud_cvas"
    title = "No votaron"
    fig = px.histogram(base, x= x,
                       histnorm='probability density',
                       title=title, 
                       labels={x:"Último dígito"},
                       width=width, height=height,
                       color_discrete_sequence=['#7F7F7F'])
    
    fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
         x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )
    
    fig.update_layout(bargap=0.2)
    col2.plotly_chart(fig, use_container_width=tamaño)
    
 ########################################################################################   
    st.header('4. EVOLUCIÓN DEL PORCENTAJE ACUMULADO DE VOTOS EN FUNCIÓN DE LA PARTICIPACIÓN') 
    
    
    
    db_part = base.groupby(['PART'])["VOTOS_P1","VOTOS_P2"].sum()

    db_part["VOTOS_VAL"]= db_part["VOTOS_P1"] + db_part["VOTOS_P2"]
    db_part['cum_PL_%'] = db_part["VOTOS_P1"].cumsum()/db_part["VOTOS_VAL"].cumsum()
    db_part['cum_FP_%'] = db_part["VOTOS_P2"].cumsum()/db_part["VOTOS_VAL"].cumsum()
    
    
    ave = np.sum(base["N_CVAS"])/np.sum(base["N_ELEC_HABIL"])
    
    
    
    fig = go.Figure(layout_title_text="POBLACIÓN TOTAL")
    
    # Add traces
    fig.add_trace(go.Scatter(x=db_part.index, y=db_part['cum_PL_%'],
                        mode='markers',
                        name='Perú Libre'))
    fig.add_trace(go.Scatter(x=db_part.index, y=db_part['cum_FP_%'],
                        mode='markers',
                        name='Fuerza Popular'))
    
    fig.add_vrect(x0=ave, x1=ave +0.005 ,col= 1,
                  annotation_text="average", annotation_position="top left",
                  fillcolor="green", opacity=0.25, line_width=0)
    
    
    col1,col2 = st.beta_columns([1,2])
    col2.plotly_chart(fig, use_container_width=True)
    
    
    #######################                       EVOLUCIÓN DEL GANADOR
    fig = go.Figure(layout_title_text="PERÚ LIBRE")
    
    # Add traces
    fig.add_trace(go.Scatter(x=db_part.index, y=db_part['cum_PL_%'],
                        mode='markers',
                        name='Perú Libre'))
    
    fig.add_vrect(x0=ave, x1=ave +0.005 ,col= 1,
                  annotation_text="average", annotation_position="top left",
                  fillcolor="green", opacity=0.25, line_width=0)
    
    
    col1.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<h5 style='text-align: center;'>Puede revisar la evoluación del porcentaje acumulado de votos por Departamento en la sección  ' Evolución % votos acumulados ' .</h5>", unsafe_allow_html=True)   
    ######################################################################  TAB PARA CADA DEPARTAMENTO
    
   #  col1,col2,col3,col4 = st.beta_columns(4)
   #  dep2= list(base[(base["AMBITO"]=="NACIONAL")]["DEPARTAMENTO"].unique())
    
   #  option = col1.selectbox('Seleccione el Departamento:', dep2)

    
   # # for itex in range(1) :          # CREACIÓN DE CADA HISTOGRAMA
   #      #mask=   (base["DEPARTAMENTO"]==dep2[itex]
   #  mask=   (base["DEPARTAMENTO"]== option ) 
   #  ave = np.sum(base[mask]["N_CVAS"])/np.sum(base[mask]["N_ELEC_HABIL"])   
   #  basdep = base[mask].groupby(['PART'])["VOTOS_P1","VOTOS_P2"].sum()
    
   #  basdep["VOTOS_VAL"]= basdep["VOTOS_P1"] + basdep["VOTOS_P2"]
   #  basdep['cum_PL_%'] = basdep["VOTOS_P1"].cumsum()/basdep["VOTOS_VAL"].cumsum()
   #  basdep['cum_FP_%'] = basdep["VOTOS_P2"].cumsum()/basdep["VOTOS_VAL"].cumsum()
        
        
   #  fig = go.Figure(layout_title_text= option )
    
   #  fig.add_trace(go.Scatter(x=basdep.index, y=basdep['cum_PL_%'],
   #                      mode='markers',
   #                      name='Perú Libre'))
        
   #  fig.add_trace(go.Scatter(x=basdep.index, y=basdep['cum_FP_%'],
   #                      mode='markers',
   #                      name='Fuerza Popular'))
    
   #  fig.add_vrect(x0=ave, x1=ave +0.005 ,col= 1,
   #                annotation_text="mean", annotation_position="top left",
   #                fillcolor="green", opacity=0.25, line_width=0)
        
   #  fig.update_layout(showlegend=True,height=400, width=500)
    
   #  col2.plotly_chart(fig, use_container_width=False)
    
    
    
    
    
    
        
    # if (itex+1)%4 == 1 :
    #             col1.plotly_chart(fig, use_container_width=False)
    # elif (itex+1)%4 == 2 :
    #             col2.plotly_chart(fig, use_container_width=False)        
    # elif (itex+1)%4 == 3 :
    #             col3.plotly_chart(fig, use_container_width=False) 
    # else:
    #         col4.plotly_chart(fig, use_container_width=False) 
            
   
    

