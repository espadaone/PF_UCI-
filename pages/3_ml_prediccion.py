import pymysql
import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import streamlit as st

connection = pymysql.connect(
    host = 'servaz.mysql.database.azure.com',
    user = 'Azadmin',
    password = 'AZcosmospf08',
    db = 'pf_uci'
  )
cursor = connection.cursor()

# Extraemos datos necesarios de admissions
cursor.execute("SELECT subject_id, admittime, dischtime, deathtime FROM admissions")
dias_admissions = pd.DataFrame(cursor, columns=('subject_id','admittime','dischtime','deathtime'))
cursor.execute("SELECT subject_id, dob, gender FROM patients")
patients = pd.DataFrame(cursor, columns=('subject_id','dob','gender'))

# Calculamos dias de hospitalizacion
dias_admissions['dias transcurridos'] = (dias_admissions['dischtime'] - dias_admissions['admittime']).dt.days
# extraemos año de ingreso, por mas que este enmascarado, para calcular la edad
dias_admissions['año ingreso'] = dias_admissions['admittime'].dt.year
# unimos id de pacientes para calcular edad
dias_admissions = dias_admissions.merge(patients[['subject_id','dob','gender']],on='subject_id')
# calculamos el año de nacimiento enmascarado nos sirve igual
dias_admissions['dob'] = dias_admissions['dob'].dt.year
# calculamos edad
dias_admissions['edad'] =dias_admissions['año ingreso'] - dias_admissions['dob']
# conservamos datos necesarios
dias_admissions = dias_admissions[['dias transcurridos','edad','deathtime','gender']]
# seteamos en 90 las edades de 300
dias_admissions['edad'][dias_admissions['edad'] == 300] = 90
# seteamos una internacion de 123 dias a 23 dias
dias_admissions['dias transcurridos'][dias_admissions['dias transcurridos'] == 123] = 23
# creamos una lista binaria para mostrar si el paciente fallecio o no
nuevos_valores = []
for i in dias_admissions['deathtime'].isna():
  if i == True:
    nuevos_valores.append(0)
  else:
    nuevos_valores.append(1)
# lo agregamos al dataset y eliminamos la columna con fecha
dias_admissions['fallecio(1=si)'] = nuevos_valores
dias_admissions = dias_admissions[['dias transcurridos','edad','fallecio(1=si)','gender']]
# creamos una lista binaria para mostrar si el paciente es hombre o mujer
genero = []
for i in dias_admissions['gender']:
  if i == 'F':
    genero.append(0)
  else:
    genero.append(1)
# lo agregamos al dataset y eliminamos la columna con fecha
dias_admissions['genero(0=Femenino)'] = genero
dias_admissions = dias_admissions[['dias transcurridos','edad','fallecio(1=si)','genero(0=Femenino)']]

X = dias_admissions[['edad','fallecio(1=si)','genero(0=Femenino)']].copy()
y = dias_admissions['dias transcurridos'].copy()
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
arbol = DecisionTreeRegressor(max_depth = 12)
arbol.fit(X_train, y_train)
Y_pred = arbol.predict(X_test)
st.subheader('Predicciones ')

scored=arbol.score(X_train, y_train)

st.metric(label="El score del modelo es:", value=round(scored*100), delta="%")


#print("El scrore del modelo es:",arbol.score(X_train, y_train))
connection.close()
fig, ax = plt.subplots(figsize = (5,6))
plt.boxplot(Y_pred)
plt.title('Prediccion de estadia de pacientes')
plt.ylabel('Estadía en días')
plt.yticks(np.linspace(Y_pred.min(),Y_pred.max(),20))
plt.grid()
st.pyplot(fig)
