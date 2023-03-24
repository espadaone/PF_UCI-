# Importamos librerias
import streamlit as st
import pymysql
import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


# Conexión a la base de datos mysql
connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'administrador',
    db = 'pf_uci'
)
cursor = connection.cursor()

# Extraemos datos necesarios de admissions
cursor.execute("SELECT subject_id, admittime, dischtime, deathtime FROM admissions")
dias_admissions = pd.DataFrame(cursor, columns=('subject_id','admittime','dischtime','deathtime'))
cursor.execute("SELECT subject_id, dob, gender FROM patients")
patients = pd.DataFrame(cursor, columns=('subject_id','dob','gender'))

connection.close()

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


st.header('Predicciones de estadia por rango etario')     # Titulo de la página


# Separador
st.markdown('--------------------------------------------------')


# Modelo
score = 0
prediccion = []
while (score < 0.85):
    X = dias_admissions[['edad','fallecio(1=si)','genero(0=Femenino)']].copy()
    y = dias_admissions['dias transcurridos'].copy()
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
    arbol = DecisionTreeRegressor(max_depth = 12)
    arbol.fit(X_train, y_train)
    Y_pred = arbol.predict(X_test)
    score = arbol.score(X_train, y_train)
    prediccion = list(Y_pred.round(0))
    
fig, ax = plt.subplots()
fig.set(figheight=4, figwidth=1.2)
plt.boxplot(prediccion)
plt.title('Predicción de estadia de pacientes (todas las edades)', fontsize=10)
plt.ylabel('Estadía en días')
plt.yticks(np.linspace(min(prediccion),max(prediccion),20).round(0))
plt.grid()
st.pyplot(fig)        


# Separador
st.markdown('--------------------------------------------------')


dias_admissions['rango etario'] = ''
dias_admissions['rango etario'][dias_admissions['edad']>0] = 'Hasta 49 años'
dias_admissions['rango etario'][dias_admissions['edad']>49] = 'De 50 a 64 años'
dias_admissions['rango etario'][dias_admissions['edad']>64] = 'De 65 a 79 años'
dias_admissions['rango etario'][dias_admissions['edad']>79] = 'Mas de 80 años'
rango_hasta49 = dias_admissions[['dias transcurridos','edad','fallecio(1=si)','genero(0=Femenino)']][dias_admissions['rango etario'] == 'Hasta 49 años']
rango_50a64 = dias_admissions[['dias transcurridos','edad','fallecio(1=si)','genero(0=Femenino)']][dias_admissions['rango etario'] == 'De 50 a 64 años']
rango_65a79 = dias_admissions[['dias transcurridos','edad','fallecio(1=si)','genero(0=Femenino)']][dias_admissions['rango etario'] == 'De 65 a 79 años']
rango_mas80 = dias_admissions[['dias transcurridos','edad','fallecio(1=si)','genero(0=Femenino)']][dias_admissions['rango etario'] == 'Mas de 80 años']

score = 0
prediccion = []
while (score < 0.8):
    X = rango_hasta49[['edad','fallecio(1=si)','genero(0=Femenino)']].copy()
    y = rango_hasta49['dias transcurridos'].copy()
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
    arbol = DecisionTreeRegressor(max_depth = 12)
    arbol.fit(X_train, y_train)
    Y_pred = arbol.predict(X_test)
    score = arbol.score(X_train, y_train)
    prediccion = list(Y_pred.round(0))
#--Grafico
fig, ax = plt.subplots()
fig.set(figheight=2.8, figwidth=1.2)
plt.boxplot(prediccion)
plt.title('Predicción de estadia de pacientes de hasta 49 años', fontsize=10)
plt.ylabel('Estadía en días')
plt.yticks(np.linspace(min(prediccion),max(prediccion),10).round(0))
plt.grid()
st.pyplot(fig)


# Separador
st.markdown('--------------------------------------------------')


# ML de 50 a 64 años
score = 0
prediccion = []
while (score < 0.8):
    X = rango_50a64[['edad','fallecio(1=si)','genero(0=Femenino)']].copy()
    y = rango_50a64['dias transcurridos'].copy()
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
    arbol = DecisionTreeRegressor(max_depth = 12)
    arbol.fit(X_train, y_train)
    Y_pred = arbol.predict(X_test)
    score = arbol.score(X_train, y_train)
    prediccion = list(Y_pred.round(0))
#-- Grafico
fig, ax = plt.subplots()
fig.set(figheight=2.8, figwidth=1.2)
plt.boxplot(prediccion)
plt.title('Predicción de estadia de pacientes de 50 a 64 años', fontsize=10)
plt.ylabel('Estadía en días')
plt.yticks(np.linspace(min(prediccion),max(prediccion),10).round(0))
plt.grid()
st.pyplot(fig)


# Separador
st.markdown('--------------------------------------------------')


# ML por rango de 65 a 79 años
score = 0
prediccion = []
while (score < 0.8):
    X = rango_65a79[['edad','fallecio(1=si)','genero(0=Femenino)']].copy()
    y = rango_65a79['dias transcurridos'].copy()
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
    arbol = DecisionTreeRegressor(max_depth = 12)
    arbol.fit(X_train, y_train)
    Y_pred = arbol.predict(X_test)
    score = arbol.score(X_train, y_train)
    prediccion = list(Y_pred.round(0))
#--Grafico
fig, ax = plt.subplots()
fig.set(figheight=2.8, figwidth=1.2)
plt.boxplot(prediccion)
plt.title('Predicción de estadia de pacientes de 65 a 79 años', fontsize=10)
plt.ylabel('Estadía en días')
plt.yticks(np.linspace(min(prediccion),max(prediccion),10).round(0))
plt.grid()
st.pyplot(fig)        


# Separador
st.markdown('--------------------------------------------------')


# ML pacientes de 80 años en adelante
score = 0
prediccion = []
while (score < 0.8):
    X = rango_mas80[['edad','fallecio(1=si)','genero(0=Femenino)']].copy()
    y = rango_mas80['dias transcurridos'].copy()
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
    arbol = DecisionTreeRegressor(max_depth = 12)
    arbol.fit(X_train, y_train)
    Y_pred = arbol.predict(X_test)
    score = arbol.score(X_train, y_train)
    prediccion = list(Y_pred.round(0))
#--Grafico
fig, ax = plt.subplots()
fig.set(figheight=2.8, figwidth=1.2)
plt.boxplot(prediccion)
plt.title('Predicción de estadia de pacientes con mas de 80 años', fontsize=10)
plt.ylabel('Estadía en días')
plt.yticks(np.linspace(min(prediccion),max(prediccion),10).round(0))
plt.grid()
st.pyplot(fig)        
