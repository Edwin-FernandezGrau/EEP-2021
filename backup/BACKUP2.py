# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 23:52:52 2021

@author: DELL
"""

# -*- coding: utf-8 -*-
"""
@author: EFERNANDEZ

"""
import streamlit as st   ### para reportear 
import pandas as pd      ### para leer base de datos 
import numpy as np       #### para operaciones numericas

st.set_page_config(page_title= "Presidencial 2021", layout="wide")

# "VOTOS_P1" = PERU LIBRE
# "VOTOS_P2" = FUERZA POPULAR




###### importamos información de los excel #################################################################################
# PARA QUE NO DEMORE LA CARGA  BASE COMPLETA
@st.cache
def get_data():
    ruta ='BASE ONPE.xlsx'    
    base = pd.read_excel(ruta,sheet_name= "BASE", header = 0,engine ='openpyxl' )
    base["PART"] = np.round(base["N_CVAS"]/base["N_ELEC_HABIL"],3) 
  # ratio de participación por mes
    base["VOTO_SHARE_FP"] = base["VOTOS_P2"]/( base["VOTOS_P2"] +base["VOTOS_P1"])  # ratio de participación por mes
    base["VOTO_SHARE_PL"] = 1-base["VOTO_SHARE_FP"] 
    
    return base

############################################################################################################################


#TITULO
st.header('Base de Datos elección presidencial 2021 - Segunda vuelta (source : https://www.datosabiertos.gob.pe/ )')

base = get_data()
#st.dataframe(base, width=1800, height=600)




#############################################################################################################################
st.header('DISTRIBUCIÓN DE ACTAS POR NUMERO DE VOTOS')

nac_ext = list(base["AMBITO"].unique()) 


## CREAMOS LA BASE 2
@st.cache
def get_data0():
    mask = (base["DESCRIP_ESTADO_ACTA"].isin(["CONTABILIZADA","COMPUTADA RESUELTA"]))
    base2= base[mask]                                             
    base2["NO_VOT"] = base2["N_ELEC_HABIL"] - base2["N_CVAS"] 
    base2["v2_ud_pl"] = base2["VOTOS_P1"].fillna(0).astype(str).str[-3].astype(int)
    base2["v2_ud_fp"] = base2["VOTOS_P2"].fillna(0).astype(str).str[-3].astype(int)
    base2["v2_ud_nul"] = base2["VOTOS_VN"].fillna(0).astype(str).str[-3].astype(int)
    base2["v2_ud_vb"] = base2["VOTOS_VB"].fillna(0).astype(str).str[-3].astype(int)
    base2["v2_ud_cvas"] = base2["N_CVAS"].fillna(0).astype(str).str[-3].astype(int)
    base2["v2_ud_nvot"] = base2["NO_VOT"].fillna(0).astype(str).str[-3].astype(int)
    
    return base2

base2 = get_data0()


####################
col1,col2 = st.beta_columns(2)
                                    # DISTRIBUCION DE VOTOS PERU LIBRE
import plotly.express as px
fig01 = px.histogram(base2,
                     x="VOTOS_P1",
                    histnorm='probability density',
                    #title='Distribución de votos por acta',
                    labels={"VOTOS_P1":'Votos Peru Libre'},
                    #color_discrete_sequence= ['orangered']# ,facet_col="DEPARTAMENTO"
                    )
# Plot!
#st.plotly_chart(fig01, use_container_width=True)
###########################

                                    # DISTRIBUCION DE VOTOS FUERZA POPULAR
fig02 = px.histogram(base2["VOTOS_P2"],
                     x="VOTOS_P2",
                     histnorm='probability density',
                    # title='Dsitribución de votos por acta',
                     labels={"VOTOS_P2":'Votos Fuerza Popular'},
                     color_discrete_sequence= ['orangered']
                   )
# Plot!
#st.plotly_chart(fig02, use_container_width=True)



col1.plotly_chart(fig01, use_container_width=True)
col2.plotly_chart(fig02, use_container_width=True)

#######################

                                        # AMBAS DISTRIBUCIONES
col1,col2,col3 = st.beta_columns([1,3,1])

import plotly.figure_factory as ff

# Add histogram data
x1 = base2["VOTOS_P2"].fillna(0)
x2 = base2["VOTOS_P1"].fillna(0)

 # Group data together
hist_data = [x1, x2]
group_labels = ['Fuerza Popular', 'Peru Libre']

# Create distplot with custom bin_size
fig03 = ff.create_distplot(
         hist_data, group_labels, bin_size=[1,1],show_rug = False, colors = ["red","blue"] 
         )
# Plot!
#st.plotly_chart(fig03, use_container_width=False)
col2.plotly_chart(fig03, use_container_width=True,)



#########################################################################################################

st.header('DISTRIBUCIÓN DE ACTAS POR VOTO COMPARTIDO %')
##### DISTRIBUCIÓN DE ACTAS POR VOTO COMPARTIDO

                                        # VOTO COMPARTIDO PERU LIBRE
col1,col2 = st.beta_columns(2)
fig01 = px.histogram(base2["VOTO_SHARE_PL"],
                     x="VOTO_SHARE_PL",
                    histnorm='probability density',
                    #title='Distribución de votos por acta',
                   # labels={"VOTOS_P1":'Votos Peru Libre'},
                    #color_discrete_sequence= ['orangered']# ,facet_col="DEPARTAMENTO"
                    )
# Plot!
#st.plotly_chart(fig01, use_container_width=True)

                                        # VOTO COMPARTIDO PERU LIBRE
fig02 = px.histogram(base2["VOTO_SHARE_FP"],
                     x="VOTO_SHARE_FP",
                     histnorm='probability density',
                    # title='Dsitribución de votos por acta',
                     #Labels={"VOTOS_P2":'Votos Fuerza Popular'},
                     color_discrete_sequence= ['orangered']
                   )
# Plot!
#st.plotly_chart(fig02, use_container_width=True)

col1.plotly_chart(fig01, use_container_width=True)
col2.plotly_chart(fig02, use_container_width=True)





##################################################################################################################
st.header('DISTRIBUCIÓN DE LOS PRIMER DÍGITO EN LOS VOTOS POR DISTRITO') 

# CREACION DE VARIABLES

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



####################################
#GRAFICAMOS LEY DE BENFORD
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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

fig.update_layout(height=500, width=1200, bargap=0.2)
st.plotly_chart(fig, use_container_width=False)



#####################################################################################################

st.header('DISTRIBUCIÓN DE ULTIMO DÍGITO EN LOS VOTOS POR DISTRITO') 


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
col1.plotly_chart(fig, use_container_width=False)


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
col2.plotly_chart(fig, use_container_width=False)



   #################                 # VOTOS NULOS
x ="v2_ud_nul"
title = "Votos nulos"
fig = px.histogram(db_ubigeo, x= x,
                   histnorm='probability density',
                   title=title, 
                   labels={x:"Último dígito"},
                   color_discrete_sequence=['#00CC96'] ,
                   width=width, height=height  )

fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
     x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )



fig.update_layout(bargap=0.2)
col3.plotly_chart(fig, use_container_width=False)

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
                   color_discrete_sequence=['#EECA3B'])

fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
     x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )

fig.update_layout(bargap=0.2)
col1.plotly_chart(fig, use_container_width=False)


##############                 # VOTOS NO FUERON
x ="v2_ud_cvas"
title = "No votaron"
fig = px.histogram(db_ubigeo, x= x,
                   histnorm='probability density',
                   title=title, 
                   labels={x:"Último dígito"},
                   width=width, height=height,
                   color_discrete_sequence=['#BAB0AC'])

fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
     x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )

fig.update_layout(bargap=0.2)
col2.plotly_chart(fig, use_container_width=False)


########################################################################################################

col1 = st.beta_columns(1) 
st.header('DISTRIBUCIÓN DE ULTIMO DÍGITO EN LOS VOTOS POR MESA') 

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
fig = px.histogram(base2, x= x, #y="total_bill", #color="sex",
                   histnorm='probability density',
                   title=title, 
                   labels={x:"Último dígito"},
                   width=width, height=height   ) 


fig.add_shape( type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )

fig.update_layout(bargap=0.2)
col1.plotly_chart(fig, use_container_width=False)


    ###############                # FUERZA POPULAR
x ="v2_ud_fp"
title = "Fuerza Popular"
fig = px.histogram(base2, x= x, #y="total_bill", #color="sex",
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
col2.plotly_chart(fig, use_container_width=False)



 ###############                   # VOTOS NULOS
x ="v2_ud_nul"
title = "Votos nulos"
fig = px.histogram(base2, x= x,
                   histnorm='probability density',
                   title=title, 
                   labels={x:"Último dígito"},
                   color_discrete_sequence=['#00CC96'] ,
                   width=width, height=height  )

fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
     x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )



fig.update_layout(bargap=0.2)
col3.plotly_chart(fig, use_container_width=False)

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
fig = px.histogram(base2, x= x,
                   histnorm='probability density',
                   title=title, 
                   labels={x:"Último dígito"},
                   width=width, height=height,
                   color_discrete_sequence=['#EECA3B'])

fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
     x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )

fig.update_layout(bargap=0.2)
col1.plotly_chart(fig, use_container_width=False)


    ###########              # VOTOS NO FUERON
x ="v2_ud_cvas"
title = "No votaron"
fig = px.histogram(base2, x= x,
                   histnorm='probability density',
                   title=title, 
                   labels={x:"Último dígito"},
                   width=width, height=height,
                   color_discrete_sequence=['#BAB0AC'])

fig.add_shape(  type="line",  line_color="salmon", line_width=3, opacity=1, line_dash="dot",
     x0=0, x1=1,xref="paper", y0=0.10, y1=0.10, yref="y"  )

fig.update_layout(bargap=0.2)
col2.plotly_chart(fig, use_container_width=False)



######################################################################################################################



st.header('% ACUMULADO DE VOTOS EN FUNCIÓN DE LA PARTICIPACIÓN') 

# dep = list(base["DEPARTAMENTO"].unique()) 
# dep_SELECT = st.multiselect("Seleccione el DEPARTAMENTO",dep , dep )

# db_part = base[base["DEPARTAMENTO"].isin(dep_SELECT)].groupby(['PART'])["VOTOS_P1","VOTOS_P2"].sum()

# db_part["VOTOS_VAL"]= db_part["VOTOS_P1"] + db_part["VOTOS_P2"]
# db_part['cum_PL_%'] = db_part["VOTOS_P1"].cumsum()/db_part["VOTOS_VAL"].cumsum()
# db_part['cum_FP_%'] = db_part["VOTOS_P2"].cumsum()/db_part["VOTOS_VAL"].cumsum()


# ave = np.sum(base["N_CVAS"])/np.sum(base["N_ELEC_HABIL"])



# fig = go.Figure()

# # Add traces
# fig.add_trace(go.Scatter(x=db_part.index, y=db_part['cum_PL_%'],
#                     mode='markers',
#                     name='Perú Libre'))
# fig.add_trace(go.Scatter(x=db_part.index, y=db_part['cum_FP_%'],
#                     mode='markers',
#                     name='Fuerza Popular'))

# fig.add_vrect(x0=ave, x1=ave +0.005 ,col= 1,
#               annotation_text="average", annotation_position="top left",
#               fillcolor="green", opacity=0.25, line_width=0)


# col1,col2,col3= st.beta_columns([1,3,1])
# col2.plotly_chart(fig, use_container_width=True)


##################################

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


######################################################################  TAB PARA CADA DEPARTAMENTO
col1,col2,col3,col4 = st.beta_columns(4)
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
    
    if (itex+1)%4 == 1 :
            col1.plotly_chart(fig, use_container_width=False)
    elif (itex+1)%4 == 2 :
            col2.plotly_chart(fig, use_container_width=False)        
    elif (itex+1)%4 == 3 :
            col3.plotly_chart(fig, use_container_width=False) 
    else:
        col4.plotly_chart(fig, use_container_width=False) 
        

#############################################################################################################

col1= st.beta_columns(1)
st.header('DISTRIBUCIÓN DE VOTOS POR DEPARTAMENTO')


genre = st.radio(                                   # DETERMINAR EL PARTIDO A GRAFICAR
    "Seleccione el Partido Político",
    ('Perú Libre', 'Fuerza Popular'))

if genre == 'Perú Libre':
    partido = "VOTOS_P1"
    colosel = ["#636EFA"]
else:
      partido = "VOTOS_P2"
      colosel = ["#EF553B"]


col1,col2,col3,col4 = st.beta_columns(4)



for itex in range(4) :          # CREACIÓN DE CADA HISTOGRAMA

    
    fig = px.histogram(base[(base["DEPARTAMENTO"]==dep2[itex])][partido], x= partido ,
                   histnorm='probability density',
                   title=dep2[itex], 
                   labels={x:genre},
                   width=width, height=height,
                   #color_discrete_sequence=[colosel]
                   )
    
    fig.update_layout(height=400, width=450)
    if (itex+1)%4 == 1 :
            col1.plotly_chart(fig, use_container_width=False)
    elif (itex+1)%4 == 2 :
            col2.plotly_chart(fig, use_container_width=False)        
    elif (itex+1)%4 == 3 :
            col3.plotly_chart(fig, use_container_width=False) 
    else:
        col4.plotly_chart(fig, use_container_width=False) 
        
        
check = st.checkbox("Mostrar más Departamentos ")
if check:

    for itex in range(4,25) :          # CREACIÓN DE CADA HISTOGRAMA
    
        
        fig = px.histogram(base[(base["DEPARTAMENTO"]==dep2[itex])][partido], x= partido ,
                       histnorm='probability density',
                       title=dep2[itex], 
                       labels={x:genre},
                       width=width, height=height,
                       #color_discrete_sequence=[colosel]
                       )
        
        fig.update_layout(height=400, width=450)
        if (itex+1)%4 == 1 :
                col1.plotly_chart(fig, use_container_width=False)
        elif (itex+1)%4 == 2 :
                col2.plotly_chart(fig, use_container_width=False)        
        elif (itex+1)%4 == 3 :
                col3.plotly_chart(fig, use_container_width=False) 
        else:
            col4.plotly_chart(fig, use_container_width=False) 