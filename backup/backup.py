# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 12:10:42 2021

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
#st.set_page_config(page_title= "Presidencial 2021",layout="wide" )


###### importamos información de los excel

# "VOTOS_P1" = PERU LIBRE
# "VOTOS_P2" = FUERZA POPULAR

ruta ='BASE ONPE.xlsx'
    
base = pd.read_excel(ruta,sheet_name= "BASE", header = 0,engine ='openpyxl' )


base["PART"] = np.round(base["N_CVAS"]/base["N_ELEC_HABIL"],3)


st.header('Base de Datos elección presidencial 2021 - Segunda vuelta (source : https://www.datosabiertos.gob.pe/ )')
#st.dataframe(base, width=1800, height=600)
st.header('Distribución de votos por Partido (en %)')


nac_ext = list(base["AMBITO"].unique()) 
nac_ext_SELECT = st.multiselect("Seleccione el Ámbito",nac_ext , nac_ext )


#ond_nac_ext = base["v2_NACIONAL_EXTRANJERO"].isin(nac_ext_SELECT)
base2 =  base[(base["AMBITO"].isin(nac_ext_SELECT)) & (base["DESCRIP_ESTADO_ACTA"].isin(["CONTABILIZADA","COMPUTADA RESUELTA"]))]





import plotly.express as px
fig01 = px.histogram(base2,
                     x="VOTOS_P1",
                    histnorm='probability density',
                    title='Dsitribución de votos por acta',
                    labels={"VOTOS_P1":'Votos Peru Libre'},
                    color_discrete_sequence=['indianred'] # ,facet_col="DEPARTAMENTO"
                    )

# Plot!
st.plotly_chart(fig01, use_container_width=True)


fig02 = px.histogram(base2["VOTOS_P2"],
                     x="VOTOS_P2",
                     histnorm='probability density',
                     title='Dsitribución de votos por acta',
                     labels={"VOTOS_P2":'Votos Fuerza Popular'},
                     color_discrete_sequence=['blue']
                     )

# Plot!
st.plotly_chart(fig02, use_container_width=True)






import plotly.figure_factory as ff

# Add histogram data
x1 = base2["VOTOS_P2"].fillna(0)
x2 = base2["VOTOS_P1"].fillna(0)

 # Group data together
hist_data = [x1, x2]
group_labels = ['Fuerza Popular', 'Peru Libre']

# Create distplot with custom bin_size
fig03 = ff.create_distplot(
         hist_data, group_labels, bin_size=[1,1],show_rug = False, colors = ["blue","red"] )

# Plot!
st.plotly_chart(fig03, use_container_width=True)





st.header('Distribución de votos por Partido (en %)')   # ley de BENFORD

db_ubigeo = base.groupby(['UBIGEO'])["VOTOS_P1","VOTOS_P2"].sum()
db_ubigeo["v2_pd_pl"] = db_ubigeo["VOTOS_P1"].astype(str).str[0].astype(int)
db_ubigeo["v2_pd_fp"] = db_ubigeo["VOTOS_P2"].astype(str).str[0].astype(int)

##########
#fig05 = px.histogram(db_ubigeo[db_ubigeo["v2_pd_pl"] != 0],
 #                   x="v2_pd_pl",
 #                   histnorm='probability density',
 #                   title='Dsitribución Perú Libre',
 #                  labels={"v2_pd_pl":'Votos Peru Libre'},
 #                  color_discrete_sequence=['red'],
 #                  )
# Plot!
#st.plotly_chart(fig05, use_container_width=False)
#
#fig06 = px.histogram(db_ubigeo[db_ubigeo["v2_pd_fp"] != 0 ],
##                    x="v2_pd_fp",
 #                   histnorm='probability density',
#                    title='Dsitribución Fuerza Popular',
#                   labels={"v2_pd_fp":'Votos Fuerza Popular'},
##                   color_discrete_sequence=['blue'], 
 #                  )
# Plot!
#st.plotly_chart(fig06, use_container_width=False)
#"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = make_subplots(rows=1, cols=2 )



# DISTRIBUCIÓN DE LOS PRIMEROS DÍGITOS EN LOS VOTOS POR DISTRITO
st.header('DISTRIBUCIÓN DE LOS PRIMEROS DÍGITOS EN LOS VOTOS POR DISTRITO') 
d1 = go.Histogram(x=db_ubigeo[db_ubigeo["v2_pd_pl"] != 0]["v2_pd_pl"], 
                                           histnorm='probability density',
                                           name = "PERU LIBRE", 
                                           )

d2 = go.Histogram(x=db_ubigeo[db_ubigeo["v2_pd_fp"] != 0]["v2_pd_fp"], 
                                           histnorm='probability density',
                                           name = "FUERZA POPULAR",
                                           )

fig.append_trace(d2  ,row = 1, col = 1)
fig.append_trace(d1  ,row = 1, col = 2)

fig.update_layout(height=500, width=1200, bargap=0.2)
st.plotly_chart(fig, use_container_width=False)





dep = list(base["DEPARTAMENTO"].unique()) 
dep_SELECT = st.multiselect("Seleccione el DEPARTAMENTO",dep , dep )

db_part = base[base["DEPARTAMENTO"].isin(dep_SELECT)].groupby(['PART'])["VOTOS_P1","VOTOS_P2"].sum()

db_part["VOTOS_VAL"]= db_part["VOTOS_P1"] + db_part["VOTOS_P2"]
db_part['cum_PL_%'] = db_part["VOTOS_P1"].cumsum()/db_part["VOTOS_VAL"].cumsum()
db_part['cum_FP_%'] = db_part["VOTOS_P2"].cumsum()/db_part["VOTOS_VAL"].cumsum()


import plotly.express as px
# iris is a pandas DataFrame
fig07 = px.scatter(db_part, x=db_part.index, y='cum_PL_%')
#fig.show()
st.plotly_chart(fig07, use_container_width=False)



fig08 = px.scatter(db_part, x=db_part.index, y='cum_FP_%')
#fig.show()
st.plotly_chart(fig08, use_container_width=False)









import plotly.graph_objects as go
from plotly.subplots import make_subplots


fig = make_subplots(rows=7, cols=4,
                    row_heights=(9,9,9,9,9,9,9))


dep2= list(base[(base["AMBITO"]=="NACIONAL")]["DEPARTAMENTO"].unique())  ## DEPARTAMENTOS - AMBITO NACIONAL


genre = st.radio(                                   # DETERMINAR EL PARTIDO A GRAFICAR
    "Seleccione el Partido Político",
   ('Perú Libre', 'Fuerza Popular'))

if genre == 'Perú Libre':
    partido = "VOTOS_P1"
else:
     partido = "VOTOS_P2"



for itex in range(25) :          # CREACIÓN DE CADA HISTOGRAMA
    globals()[f"trace{itex}"] = go.Histogram(x=base[(base["DEPARTAMENTO"]==dep2[itex])][partido], 
                                           histnorm='probability density',
                                           name = dep2[itex]
                                           )

trace25 = go.Histogram(x=base[(base["AMBITO"]=="EXTRANJERO")][partido], 
                                           histnorm='probability density',
                                           name = "EXTRANJERO"
                                           )

                                             # UBICACIÓN DE CADA DEPARTAMENTO
fig.append_trace(trace0  ,row = 1, col = 1)
fig.append_trace(trace1  ,row = 1, col = 2)
fig.append_trace(trace2  ,row = 1, col = 3)
fig.append_trace(trace3  ,row = 1, col = 4)

fig.append_trace(trace4  ,row = 2, col = 1)
fig.append_trace(trace5  ,row = 2, col = 2)
fig.append_trace(trace6  ,row = 2, col = 3)
fig.append_trace(trace7  ,row = 2, col = 4)

fig.append_trace(trace8  ,row = 3, col = 1)
fig.append_trace(trace9  ,row = 3, col = 2)
fig.append_trace(trace10  ,row = 3, col = 3)
fig.append_trace(trace11  ,row = 3, col = 4)

fig.append_trace(trace12  ,row = 4, col = 1)
fig.append_trace(trace13  ,row = 4, col = 2)
fig.append_trace(trace14  ,row = 4, col = 3)
fig.append_trace(trace15  ,row = 4, col = 4)

fig.append_trace(trace16  ,row = 5, col = 1)
fig.append_trace(trace17  ,row = 5, col = 2)
fig.append_trace(trace18  ,row = 5, col = 3)
fig.append_trace(trace19  ,row = 5, col = 4)


fig.append_trace(trace20  ,row = 6, col = 1)
fig.append_trace(trace21  ,row = 6, col = 2)
fig.append_trace(trace22  ,row = 6, col = 3)
fig.append_trace(trace23  ,row = 6, col = 4)

fig.append_trace(trace24  ,row = 7, col = 1)
fig.append_trace(trace25  ,row = 7, col = 2)

fig.update_layout(height=1500, width=1500)    # TAMAÑO DE LA FIGURA GRANDE
#fig.show()

st.plotly_chart(fig, use_container_width=False)


