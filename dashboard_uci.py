# Importamos librerias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
from datetime import datetime
import streamlit.components.v1 as components
import os

st.set_page_config(page_title='UCI: Dashboard general', page_icon=':hospital:')

# Conexion con ddbb
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
cursor.execute("select hadm_id, subject_id, admittime, dischtime, deathtime, admission_type, diagnosis from admissions")
admissions = pd.DataFrame(cursor, columns=("hadm_id", "subject_id", "admittime", "dischtime", "deathtime", "admission_type", "diagnosis"))

cursor.execute("select subject_id, gender, insurance, dob from patients")
patients = pd.DataFrame(cursor, columns=("subject_id", "gender", "insurance", "dob"))

cursor.execute("select prescriptions_id, drug from prescriptions")
prescriptions = pd.DataFrame(cursor, columns=("prescriptions_id", "drug"))

#Datos para tasa de mortalidad por rango etario
cursor.execute("SELECT hospital_expire_flag FROM admissions")
mortalidad_rango_etario = pd.DataFrame(cursor, columns=['hospital_expire_flag'])

# Datos para calcular duración de estancia por diagnostico
cursor.execute("SELECT diagnosis, avg(timestampdiff(day, admittime, dischtime)) FROM admissions group by 1;")
estancia_byDiagnosis = cursor.fetchall()

#Datos para promedio de estadia
cursor.execute(
    "SELECT subject_id, timestampdiff(day, admittime, dischtime) FROM admissions;"
)
data_estadia = pd.DataFrame(cursor, columns=('subject_id','estadia'))
promedio_estadia = data_estadia['estadia'].values.mean()
promedio_estadia = promedio_estadia.round(0)

cursor.execute("SELECT count(*), month(admittime) from admissions group by 2 order by 2 asc")
data_adm_mes = cursor.fetchall()




st.title('Estadisticas generales')     # Titulo de la página
st.image('images/estadistica.jpg', width=700)


# Separador
st.markdown('--------------------------------------------------')

st.subheader('Clasificación de pacientes por género')
col1, col2 = st.columns(2)
genero = patients['gender'].value_counts()
genero_df = pd.DataFrame(data=genero)
genero_df['porcentaje'] = (genero_df['gender']/genero_df['gender'].sum()) * 100
fig, ax = plt.subplots()
fig.set(figheight=2, figwidth=2)
x = genero_df['porcentaje']
colors = ['pink', 'aqua']
labels = genero.index
text_prop = {'family':'sans-serif', 'fontsize':10, 'fontstyle':'italic', 'fontweight':'heavy'}
ax.pie(x, colors=colors, labels=labels, radius=1, labeldistance=0.3, autopct="%1.0f%%", center=(4, 4), wedgeprops={"linewidth": 1, "edgecolor": "white"}, textprops=text_prop)

with col1:
    st.pyplot(fig)
with col2:
    print('')



# Separador
st.markdown('--------------------------------------------------')

st.subheader('Top 5: Diagnósticos más comunes')
top_enfermedades = admissions["diagnosis"].value_counts().head().sort_values('index', ascending=True)
enfermedades_df = pd.DataFrame(data=top_enfermedades)
#--Gráfico
fig, ax = plt.subplots()
fig.set(figheight=2, figwidth=5)
x = enfermedades_df.index
y = enfermedades_df["diagnosis"]
ax.barh(x, y, color=["yellowgreen","salmon","tan","coral","lavender"])
st.pyplot(fig)        


# Separador
st.markdown('--------------------------------------------------')

st.subheader('Top 5: Drogas más recetadas')
pre = prescriptions["drug"].value_counts().head().sort_values('index', ascending=True)
prescriptions_df = pd.DataFrame(data=pre)
#--Gráfico
fig, ax = plt.subplots()
fig.set(figheight=2, figwidth=5)
x = prescriptions_df.index
y = prescriptions_df["drug"]
ax.barh(x, y, color=["yellowgreen","orchid","pink","coral","aqua"])
st.pyplot(fig)


# Separador
st.markdown('--------------------------------------------------')


st.subheader('Admisiones por seguro médico')
admissions_insurance = pd.merge(left=admissions, right=patients, left_on='subject_id', right_on='subject_id', how='left')
admissions_insurance = admissions_insurance.groupby('insurance').count()
admissions_insurance['insurance'] =  admissions_insurance.index
admissions_insurance.reset_index(drop = True, inplace = True)
admissions_insurance.rename(columns={'hadm_id': 'count'}, inplace=True)
admissions_insurance = admissions_insurance[['insurance', 'count']]
admissions_insurance = admissions_insurance.sort_values('count', ascending=False)
fig, ax = plt.subplots()
fig.set(figheight=2, figwidth=5)
x = admissions_insurance['insurance']
y = admissions_insurance['count']
ax.bar(x, y)
st.pyplot(fig)


# Separador
st.markdown('--------------------------------------------------')


# Fallecidos por mes
st.subheader('Pacientes fallecidos por mes')
mes_fallecimiento = st.slider('Mes de fallecimiento', 1, 12, value=(1, 12))  # min: 1 mes, max: 12 meses
admissions.dropna(inplace=True)
admissions["month"] = admissions["deathtime"].apply(lambda x: datetime.date(x).month)
admissions_byMonth = admissions.groupby('month', as_index=False).count().sort_values(by='month')
admissions_byMonth = admissions_byMonth[['month', 'hadm_id']]
admissions_byMonth.rename(columns={'hadm_id': 'count'}, inplace=True)
filtro_fallecimiento = admissions_byMonth[(admissions_byMonth['month'] >= mes_fallecimiento[0]) & (admissions_byMonth['month'] <= mes_fallecimiento[1])] 
#--Gráfico
fig, ax = plt.subplots()
fig.set(figheight=3, figwidth=6)
x = filtro_fallecimiento['month']
y = filtro_fallecimiento['count']
ax.grid()
ax.set(xlabel="Mes", ylabel="N° de fallecidos")
plt.plot(x, y, marker="o")
st.pyplot(fig)


# Separador
st.markdown('--------------------------------------------------')


st.subheader('Admisiones por mes')
mes_admision = st.slider('Mes de admisión', 1, 12, value=(1, 12))  # min: 1 mes, max: 12 meses
adm_mes = pd.DataFrame(data=data_adm_mes, columns=["cantidad", "mes"])
filtro_admision = adm_mes[(adm_mes['mes'] >= mes_admision[0]) & (adm_mes['mes'] <= mes_admision[1])] 
#admisiones por mes
fig, ax = plt.subplots()
fig.set(figheight=3, figwidth=6)
x = filtro_admision["mes"]
y = filtro_admision["cantidad"]
ax.grid()
ax.set(xlabel="Meses", ylabel="N° de admisiones")
plt.plot(x, y, marker="o")
st.pyplot(fig)



# Separador
st.markdown('--------------------------------------------------')


st.subheader('Duración media de estancia por diagnóstico')
admissions_diagnosis = admissions[['diagnosis', 'admittime', 'dischtime']]
admissions_diagnosis['admittime'] = pd.to_datetime(admissions_diagnosis['admittime']).dt.date
admissions_diagnosis['dischtime'] = pd.to_datetime(admissions_diagnosis['dischtime']).dt.date
admissions_diagnosis['lenght_stay'] = admissions_diagnosis['dischtime'] - admissions_diagnosis['admittime']
lenght_prom_diagnoses = admissions_diagnosis.groupby('diagnosis', as_index=False).mean()
lenght_prom_diagnoses = lenght_prom_diagnoses[['diagnosis', 'lenght_stay']]
lenght_prom_diagnoses = lenght_prom_diagnoses.sort_values('lenght_stay', ascending=True).tail()
lenght_prom_diagnoses['lenght_stay'] = lenght_prom_diagnoses['lenght_stay'].dt.days
#--Gráfico
fig, ax = plt.subplots()
fig.set(figheight=2, figwidth=5)
x = lenght_prom_diagnoses['diagnosis']
y = lenght_prom_diagnoses['lenght_stay']
ax.barh(x, y, color=["yellowgreen","orchid","pink","coral","aqua"])
ax.set(xlabel="Días promedio de estancia")
st.pyplot(fig)


# Separador
st.markdown('--------------------------------------------------')


st.subheader('Duración media de la estancia en el hospital :ambulance:')

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

# Agregamos rango etario a la tabla
data_estadia['rango etario'] = edad['rango etario']
data_estadia['edad'] = edad['edad']
# calculamos promedio de la estadia por rango etario, estarán ordenados por rango etario de menor a mayor
estadia_rango_etario = []
rangos = ['<= 30 años','30 a 49 años','50 a 64 años','65 a 79 años','>= 80 años']
for indice_rango_etario in range(5):
    total_estadia = []
    validador_rango = rangos[indice_rango_etario]
    for indice in data_estadia.index:
        if data_estadia['rango etario'][indice] == validador_rango:
            total_estadia.append(data_estadia['estadia'][indice])
    total_estadia = pd.DataFrame(total_estadia)
    estadia_rango_etario.append(total_estadia[0].mean())
# pasamos los datos a un df
df_estadia_rango = pd.DataFrame(estadia_rango_etario)
df_estadia_rango = df_estadia_rango.rename(columns={0:'Estadia'})
df_estadia_rango['Rango etario'] = ['<= 30','30 a 49','50 a 64','65 a 79','>= 80']
# los ordenamos para el grafico de pareto
df_estadia_rango = df_estadia_rango.sort_values('Estadia',ascending=False)
# calculamos freq(%) y cum(%) para graficar
df_estadia_rango['Freq(%)'] = df_estadia_rango['Estadia']/df_estadia_rango['Estadia'].sum()*100
df_estadia_rango['cum(%)'] = df_estadia_rango['Estadia'].cumsum()/df_estadia_rango['Estadia'].sum()*100
# Reseteamos indice para facilitar titulos de barras
df_estadia_rango.reset_index(inplace=True)
df_estadia_rango.drop(columns=("index"), inplace=True)
# Graficamos
fig, ax = plt.subplots(figsize=(8,6))
ax.bar(df_estadia_rango['Rango etario'], df_estadia_rango['Freq(%)'])
#ax2 = ax.twinx()
#ax2.plot(df_estadia_rango['Rango etario'], df_estadia_rango['cum(%)'], color="g", marker="o", ms=5)
ax.annotate(("Estadia\npromedio\n{}".format(df_estadia_rango['Estadia'][0].round(2))),(0,(df_estadia_rango['Freq(%)'][0].round(2)/2)),ha='center')
ax.annotate(("Estadia\npromedio\n{}".format(df_estadia_rango['Estadia'][1].round(2))),(1,(df_estadia_rango['Freq(%)'][1].round(2)/2)),ha='center')
ax.annotate(("Estadia\npromedio\n{}".format(df_estadia_rango['Estadia'][2].round(2))),(2,(df_estadia_rango['Freq(%)'][2].round(2)/2)),ha='center')
ax.annotate(("Estadia\npromedio\n{}".format(df_estadia_rango['Estadia'][3].round(2))),(3,(df_estadia_rango['Freq(%)'][3].round(2)/2)),ha='center')
ax.annotate(("Estadia\npromedio\n{}".format(df_estadia_rango['Estadia'][4].round(2))),(4,(df_estadia_rango['Freq(%)'][4].round(2)/2)),ha='center')
plt.title("Estadía media por rango etario")
plt.ylabel('Días')
st.pyplot(fig)

# Separador
st.markdown('--------------------------------------------------')
connection.close()