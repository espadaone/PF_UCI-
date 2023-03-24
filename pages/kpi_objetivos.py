# Importamos librerias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
from datetime import datetime
import os

st.set_page_config(page_title='UCI: KPIs y objetivos \01F3AF', page_icon=':hospital:')

# Obtener credenciales desde las variables de entorno
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

# Conexion con ddbb
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    db=db_name
)
cursor = connection.cursor()

# Traemos datos desde la base de datos y guardamos las tablas a usar en datasets.
#Datos para tabla rango etario
cursor.execute("SELECT subject_id, admittime, dischtime, deathtime FROM admissions")
admissions = pd.DataFrame(cursor, columns=('subject_id','admittime','dischtime','deathtime'))
cursor.execute("SELECT subject_id, dob, gender FROM patients")
patients = pd.DataFrame(cursor, columns=('subject_id','dob','gender'))

#Datos para tasa de readmision
cursor.execute('SELECT subject_id, admittime FROM admissions')
tabla_readmision = pd.DataFrame(cursor, columns=('subject_id','admittime'))


#Datos para tasa de supervivencia
cursor.execute("SELECT hospital_expire_flag, count(hospital_expire_flag) FROM pf_uci.admissions group by 1")
data = cursor.fetchall()
tasa_supervivencia = pd.DataFrame(data=data, columns=["estado", "cantidad"])
suma = tasa_supervivencia["cantidad"].sum()
sobrevivientes = tasa_supervivencia.loc[0,"cantidad"]
tasa_supervivencia = sobrevivientes/suma
tasa_supervivencia = tasa_supervivencia.round(2)
tasa_mortalidad = (1 - tasa_supervivencia).round(3)

#Datos para tasa de mortalidad por rango etario
cursor.execute("SELECT hospital_expire_flag FROM admissions")
mortalidad_rango_etario = pd.DataFrame(cursor, columns=['hospital_expire_flag'])

#Datos para tasa de admisiones con seguro privado
cursor.execute(
    "SELECT insurance, count(*) FROM patients group by 1"
)
data = cursor.fetchall()
insurance = pd.DataFrame(data=data, columns=["insurance", "cantidad"])
total = insurance["cantidad"].sum()
priv = insurance["insurance"] == "Private"
privado = insurance.loc[priv]["cantidad"].sum()
tasa_seg_privado = privado/total


# Datos para tasa de personas con insurance privado
cursor.execute("SELECT insurance, count(*) FROM patients group by 1")
data = cursor.fetchall()
insurance = pd.DataFrame(data=data, columns=["insurance", "cantidad"])

#Tasa de cancelaciones del subconjunto de pacientes que fueron monitoriados con el sistema iMDSoft Metavision
cursor = connection.cursor()
cursor.execute("SELECT cancelreason, count(*) FROM procedureevents_mv group by 1")
data = cursor.fetchall()

#Datos para promedio de estadia
cursor.execute("SELECT subject_id, timestampdiff(day, admittime, dischtime) FROM admissions;")
data_estadia = pd.DataFrame(cursor, columns=('subject_id','estadia'))
promedio_estadia = data_estadia['estadia'].values.mean()
promedio_estadia = promedio_estadia.round(0)




st.title('KPIs y objetivos del negocio')     # Titulo de la página
st.image('images/objetivos.jpg', width=700)

# Separador
st.markdown('--------------------------------------------------')

st.subheader('KPIs principales')
st.markdown('Valores expresados en porcentaje (%)')
col1, col2 = st.columns(2)
with col1:
    st.metric(':green_book: ***Tasa supervivencia***', tasa_supervivencia*100, '2%')       
with col2:
    st.metric(':closed_book: ***Tasa mortalidad***', tasa_mortalidad*100, '-2%')

col1, col2 = st.columns(2)
with col1:
    #Tasa de personas con insurance privado
    total = insurance["cantidad"].sum()
    priv = insurance["insurance"] == "Private"
    privado = insurance.loc[priv]["cantidad"].sum()
    tasa = privado/total
    st.metric(':credit_card: ***Pacientes con seguro privado***', tasa*100, '-5%')
with col2:
    cancelaciones_mv = pd. DataFrame(data=data, columns=["cancelreason", "cantidad"])
    total = cancelaciones_mv["cantidad"].sum()
    mascara = cancelaciones_mv["cancelreason"] != 0
    cancelaciones = cancelaciones_mv[mascara]["cantidad"].sum()
    tasa = cancelaciones/total
    st.metric(':x: ***Tasa de cancelación***', round(tasa*100,1), '-+0,7%')

col1, col2 = st.columns(2)
with col1:
    # admisiones totales
    admisiones = len(tabla_readmision)
    # readmisiones
    readmisiones = admisiones - (len(tabla_readmision['subject_id'].unique()))
    # calculamos tasa de readmision anual
    tasa_readmision_anual = readmisiones/admisiones
    st.metric(':back: ***Tasa de readmisión***', round(tasa_readmision_anual*100,1), '+-1,7%')
with col2:
    st.metric(':closed_book: ***Estadia promedio (días)***', promedio_estadia, '+-2%')


# Separador
st.markdown('--------------------------------------------------')

st.subheader('Tasa de readmision :back:')

# Calculo de rango etario
edad = admissions[['subject_id','admittime']]
edad['añoIngreso'] = edad['admittime'].dt.year
edad = edad.merge(patients[['subject_id','dob']],on='subject_id')
edad['dob'] = edad['dob'].dt.year
edad['edad'] = edad['añoIngreso'] - edad['dob']
edad = edad[['subject_id','edad']]
edad['edad'][edad['edad'] == 300] = 90
edad['rango etario'] = ''
edad['rango etario'][edad['edad']>0] = '<= 30 años'
edad['rango etario'][edad['edad']>29] = '30 a 49 años'
edad['rango etario'][edad['edad']>49] = '50 a 64 años'
edad['rango etario'][edad['edad']>64] = '65 a 79 años'
edad['rango etario'][edad['edad']>79] = '>= 80 años'


# admisiones totales
admisiones = len(tabla_readmision)
# readmisiones
readmisiones = admisiones - (len(tabla_readmision['subject_id'].unique()))
# calculamos tasa de readmision anual
tasa_readmision_anual = readmisiones/admisiones
# Agregamos rango etario a la tabla
tabla_readmision['rango etario'] = edad['rango etario']
tabla_readmision['edad'] = edad['edad']
# contamos la cantidad de ingresos por rango etario, estarán ordenados por rango etario de menor a mayor
ingresos_rango_etario = []
rangos = ['<= 30 años','30 a 49 años','50 a 64 años','65 a 79 años','>= 80 años']
for indice_rango_etario in range(5):
    cant_ingresos = 0
    validador_rango = rangos[indice_rango_etario]
    for validador in tabla_readmision['rango etario']:
        if validador == validador_rango:
            cant_ingresos += 1
    ingresos_rango_etario.append(cant_ingresos)
# Separamos los datos de readmision
readmitidos = pd.DataFrame(columns=('subject_id','rango etario'))
for indice in range(128):
    if tabla_readmision['subject_id'].duplicated().iloc[indice] == True:
        readmitidos = readmitidos.append(tabla_readmision.iloc[indice])
# contamos la cantidad de reingresos por rango etario, estarán ordenados por rango etario de menor a mayor
reingresos_rango_etario = []
for indice_rango_etario in range(5):
    cant_ingresos = 0
    validador_rango = rangos[indice_rango_etario]
    for validador in readmitidos['rango etario']:
        if validador == validador_rango:
            cant_ingresos += 1
    reingresos_rango_etario.append(cant_ingresos)
# calculamos la tasa de readmision para cada rango etario, estarán ordenados por rango etario menor a mayor
tasa_readmision_rango_etario = []
for indice in range(5):
    tasa_readmision_rango_etario.append(reingresos_rango_etario[indice] / ingresos_rango_etario[indice])
# pasamos los datos a un df
df_tasa_rango = pd.DataFrame(tasa_readmision_rango_etario)
df_tasa_rango = df_tasa_rango.rename(columns={0:'Tasa'})
df_tasa_rango['Rango etario'] = ['<= 30','30 a 49','50 a 64','65 a 79','>= 80']
# los ordenamos para el grafico de pareto
df_tasa_rango = df_tasa_rango.sort_values('Tasa',ascending=False)
# calculamos freq(%) y cum(%) para graficar
df_tasa_rango['Freq(%)'] = df_tasa_rango['Tasa']/df_tasa_rango['Tasa'].sum()*100
df_tasa_rango['cum(%)'] = df_tasa_rango['Tasa'].cumsum()/df_tasa_rango['Tasa'].sum()*100
# Redondeamos tasa de readmision para grafico mas presentable
df_tasa_rango['Tasa'] = df_tasa_rango['Tasa'].round(3)
# Reseteamos indice para facilitar titulos de barras
df_tasa_rango.reset_index(inplace=True)
df_tasa_rango.drop(columns=("index"), inplace=True)
# Graficamos
fig, ax = plt.subplots(figsize=(6,4))
ax.bar(df_tasa_rango['Rango etario'], df_tasa_rango['Freq(%)'])
#ax2 = ax.twinx()
#ax2.plot(df_tasa_rango['Rango etario'], df_tasa_rango['cum(%)'], color="g", marker="o", ms=5)
ax.annotate(("Tasa\nreadmision\n{}".format(df_tasa_rango['Tasa'][0])),(0,(df_tasa_rango['Freq(%)'][0].round(2)/2)),ha='center')
ax.annotate(("Tasa\nreadmision\n{}".format(df_tasa_rango['Tasa'][1])),(1,(df_tasa_rango['Freq(%)'][1].round(2)/2)),ha='center')
ax.annotate(("Tasa\nreadmision\n{}".format(df_tasa_rango['Tasa'][2])),(2,(df_tasa_rango['Freq(%)'][2].round(2)/2)),ha='center')
ax.annotate(("Tasa\nreadmision\n{}".format(df_tasa_rango['Tasa'][3])),(3,(df_tasa_rango['Freq(%)'][3].round(2)/2)),ha='center')
ax.annotate(("Tasa\nreadmision\n{}".format(df_tasa_rango['Tasa'][4])),(4,(df_tasa_rango['Freq(%)'][4].round(2)/2)),ha='center')
plt.title("Tasa de readmision por rango etario")
st.pyplot(fig)


# Separador
st.markdown('--------------------------------------------------')

st.subheader(':closed_book: Tasa mortalidad')
# Agregamos rango etario a la tabla
mortalidad_rango_etario['rango etario'] = edad['rango etario']
cant_admisiones = len(mortalidad_rango_etario)
mortalidad_rango_etario = mortalidad_rango_etario.groupby('rango etario').sum()
mortalidad_rango_etario['tasa mortalidad'] = mortalidad_rango_etario['hospital_expire_flag']/cant_admisiones
mortalidad_rango_etario = mortalidad_rango_etario.rename({'30 a 49 años':'30-49','50 a 64 años':'50 a 64','65 a 79 años':'65 a 79','<= 30 años':'Hasta 30','>= 80 años':'+ 80'})
mortalidad_rango_etario = mortalidad_rango_etario.sort_values('hospital_expire_flag', ascending=False)
fig, ax = plt.subplots(figsize=(6,4))
plt.bar(mortalidad_rango_etario.index,mortalidad_rango_etario['tasa mortalidad'])
plt.title('Tasa de mortalidad por rango etario')
plt.xlabel('Edad')
st.pyplot(fig)
connection.close()  # Cierre de conexión con la base de datos