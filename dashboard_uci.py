# Importamos librerias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql


# Conexion con ddbb
connection = pymysql.connect(
    host='servaz.mysql.database.azure.com',
    user='Azadmin',
    password='AZcosmospf08',
    db='pf_uci'
)
cursor = connection.cursor()

# Traemos datos desde la base de datos y guardamos las tablas a usar en datasets.
cursor.execute("select hadm_id, subject_id, admittime, admission_type, diagnosis from admissions")
admissions = pd.DataFrame(cursor, columns=("hadm_id", "subject_id", "admittime", "admission_type", "diagnosis"))

cursor.execute("select subject_id, gender, insurance, dob from patients")
patients = pd.DataFrame(cursor, columns=("subject_id", "gender", "insurance", "dob"))

#cursor.execute("select prescriptions_id, drug from prescriptions")
#prescriptions = pd.DataFrame(cursor, columns=("prescriptions_id", "drug"))


st.title('Estadisticas generales')     # Titulo de la app

st.subheader('Pacientes por genero')
genero = patients['gender'].value_counts()
genero_df = pd.DataFrame(data=genero)
genero_df['porcentaje'] = (genero_df['gender']/genero_df['gender'].sum()) * 100
fig, ax = plt.subplots()
x = genero_df['porcentaje']
colors = ['pink', 'aqua']
labels = genero.index
text_prop = {'family':'sans-serif', 'fontsize':'medium', 'fontstyle':'italic', 'fontweight':'heavy'}
ax.pie(x, colors=colors, labels=labels, radius=0.6, labeldistance=0.3, autopct="%1.0f%%", center=(4, 4), wedgeprops={"linewidth": 2, "edgecolor": "white"}, textprops=text_prop)
st.pyplot(fig)


st.subheader('Enfermedades mas comunes')
top_enfermedades = admissions["diagnosis"].value_counts().head()
enfermedades_df = pd.DataFrame(data=top_enfermedades)
enfermedades_df
fig, ax = plt.subplots()
x = enfermedades_df.index
y = enfermedades_df["diagnosis"]
ax.barh(x, y, color=["yellowgreen","salmon","tan","coral","lavender"])
st.pyplot(fig)


#st.subheader('Drogas mas recetadas')
#pre = prescriptions["drug"].value_counts().head()
#prescriptions_df = pd.DataFrame(data=pre)
#prescriptions_df
#fig, ax = plt.subplots()
#x = prescriptions_df.index
#y = prescriptions_df["drug"]
#ax.barh(x, y, color=["yellowgreen","orchid","pink","coral","aqua"])
#st.pyplot(fig)


st.subheader('Duracion media de estancia por diagnostico')


st.subheader('Admisiones por insurance')


st.subheader('Pacientes vs cuidadores')


st.subheader('Tabla de rango etario pacientes')

#cursor = connection.cursor()
cursor.execute("SELECT subject_id, admittime, dischtime, deathtime FROM admissions")
admissions = pd.DataFrame(cursor, columns=('subject_id','admittime','dischtime','deathtime'))
cursor.execute("SELECT subject_id, dob, gender FROM patients")
patients = pd.DataFrame(cursor, columns=('subject_id','dob','gender'))
#connection.close()
edad = admissions[['subject_id','admittime']]
edad['añoIngreso'] = edad['admittime'].dt.year
edad = edad.merge(patients[['subject_id','dob']],on='subject_id')
edad['dob'] = edad['dob'].dt.year
edad['edad'] = edad['añoIngreso'] - edad['dob']
edad = edad[['subject_id','edad']]
edad['edad'][edad['edad'] == 300] = 90
edad['rango etario'] = ''
edad['rango etario'][edad['edad']>0] = 'Hasta 30 años'
edad['rango etario'][edad['edad']>29] = 'De 30 a 49 años'
edad['rango etario'][edad['edad']>49] = 'De 50 a 64 años'
edad['rango etario'][edad['edad']>64] = 'De 65 a 79 años'
edad['rango etario'][edad['edad']>79] = 'Mas de 80 años'

#cursor = connection.cursor()

# Tasa de readmision
cursor.execute('SELECT subject_id, admittime FROM admissions')
tabla_readmision = pd.DataFrame(cursor, columns=('subject_id','admittime'))
#connection.close()

# admisiones totales
admisiones = len(tabla_readmision)
# readmisiones
readmisiones = admisiones - (len(tabla_readmision['subject_id'].unique()))
# calculamos tasa de readmision anual
tasa_readmision_anual = readmisiones/admisiones
# Agregamos rango etario a la tabla
tabla_readmision['rango etario'] = edad['rango etario']
tabla_readmision['edad'] = edad['edad']
# contamos la cantidad de ingresos por rango etario, estarán ordenados de menor a mayor
ingresos_rango_etario = []
rangos = ['Hasta 30 años','De 30 a 49 años','De 50 a 64 años','De 65 a 79 años','Mas de 80 años']
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
# contamos la cantidad de reingresos por rango etario, estarán ordenados de menor a mayor
reingresos_rango_etario = []
for indice_rango_etario in range(5):
    cant_ingresos = 0
    validador_rango = rangos[indice_rango_etario]
    for validador in readmitidos['rango etario']:
        if validador == validador_rango:
            cant_ingresos += 1
    reingresos_rango_etario.append(cant_ingresos)
# calculamos la tasa de readmision para cada rango etario, estarán ordenados de menor a mayor
tasa_readmision_rango_etario = []
for indice in range(5):
    tasa_readmision_rango_etario.append(reingresos_rango_etario[indice] / ingresos_rango_etario[indice])
# graficamos
fig, ax = plt.subplots(figsize = (6,4))
rangos
plt.bar(['Hasta 30','De 30 a 49','De 50 a 64','De 65 a 79','Más de 80'],tasa_readmision_rango_etario)
plt.xlabel('Rango etario')
plt.yticks(np.linspace(0,max(tasa_readmision_rango_etario),10))
plt.ylabel('Tasa de readmision')
st.pyplot(fig)
#plt.show()
# Tasa de readmision anual
st.metric(label="Tasa de readmision anual", value=round(tasa_readmision_anual*100), delta="%")
#print("Tasa de readmision anual",)

st.subheader('Tabla de readmision mensual de pacientes')
# extraemos los meses
tabla_readmision['admitmonth'] = tabla_readmision['admittime'].dt.month
# admisiones totales
admisiones = len(tabla_readmision)
# readmisiones
readmisiones = admisiones - (len(tabla_readmision['subject_id'].unique()))
# calculamos tasa de readmision anual
tasa_readmision_anual = readmisiones/admisiones
# contamos la cantidad de ingresos por cada mes, estarán ordenados de enero a diciembre
vector_ingreso_mes = []
mes = 1
while mes < 13:
    contador = 0
    for validador in tabla_readmision['admitmonth']:
        if validador == mes:
            contador += 1
    vector_ingreso_mes.append(contador)
    mes += 1
# separamos los registros de readmisiones
readmitidos = pd.DataFrame(columns=('subject_id','admittime','admitmonth'))
for indice in range(128):
    if tabla_readmision['subject_id'].duplicated().iloc[indice] == True:
        readmitidos = readmitidos.append(tabla_readmision.iloc[indice])
# contamos la cantidad de reingresos por cada mes, estarán ordenados de enero a diciembre
vector_reingreso_mes = []
mes = 1
while mes < 13:
    contador = 0
    for validador in readmitidos['admitmonth']:
        if validador == mes:
            contador += 1
    vector_reingreso_mes.append(contador)
    mes += 1
# contamos la tasa de readmision para cada mes, estarán ordenados de enero a diciembre
tasa_readmision_mensual = []
for indice in range(12):
    tasa_readmision_mensual.append(vector_reingreso_mes[indice] / vector_ingreso_mes[indice])
# Graficamos

fig, ax = plt.subplots(figsize = (6,4))
meses = [1,2,3,4,5,6,7,8,9,10,11,12]
plt.plot(meses,tasa_readmision_mensual, label = 'Tasa de readmision mensual')
plt.xticks(np.linspace(1,12,12))
plt.xlabel('Meses')
plt.yticks(np.linspace(min(tasa_readmision_mensual),max(tasa_readmision_mensual),10))
plt.ylabel('Tasa de readmision')
plt.grid()
plt.legend()
#plt.show()
st.pyplot(fig)
# Tasa de readmision anual
#st.metric(label="Tasa de readmision mensual", value=f'{tasa_readmision_mensual:.2f}', delta="%")
#print("Tasa de readmision anual",tasa_readmision_anual)

st.subheader("Promedio Estadia")

cursor.execute("SELECT timestampdiff(day, admittime, dischtime) FROM admissions")
data = pd.DataFrame(cursor)
promedio_estadia = data.values.mean()
#connection.close()
#promedio_estadia
st.metric(label="Promedio ", value=round(promedio_estadia*100), delta="dias")

st.subheader('Tasa mortalidad')

cursor.execute("SELECT hospital_expire_flag, count(hospital_expire_flag) FROM pf_uci.admissions group by 1")
data = cursor.fetchall()
tasa_supervivencia = pd.DataFrame(data=data, columns=["estado", "cantidad"])
suma = tasa_supervivencia["cantidad"].sum()
sobrevivientes = tasa_supervivencia.loc[0,"cantidad"]
tasa_supervivencia = sobrevivientes/suma
connection.close()
#tasa_supervivencia
st.metric(label="Tasa de supervivencia ", value=round(tasa_supervivencia*100), delta="%")
