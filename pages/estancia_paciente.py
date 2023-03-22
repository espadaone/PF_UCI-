# Importamos librerias
import streamlit as st
import pandas as pd
import numpy as np
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


st.title('Estancia del paciente')     # Titulo de la app
#admissions = pd.read_csv(r'datasets\ADMISSIONS.csv')    # Cargamos el dataset


st.subheader('Tabla admissions con los datos de la hospitalización')
hadm_id = st.number_input('Ingrese numero de admision:', min_value=0, max_value=999999) # Input para ingresar n° de hospitalización
admissions_hadm = admissions.loc[ admissions['hadm_id'] == hadm_id ]        # Filtra los registros que coincidan con el hadm_id ingresado.
st.write(admissions_hadm)       # Muestra la tabla filtrada

paciente = admissions.loc[ admissions['hadm_id'] == hadm_id ]
st.write('Paciente: ', paciente['subject_id'].values[0])

st.subheader('Edad:')

tipo_admision = admissions.loc[ admissions['hadm_id'] == hadm_id ]
st.write('Tipo de admisión: ', tipo_admision['admission_type'].values[0])

diagnostico = admissions.loc[ admissions['hadm_id'] == hadm_id ]
st.write('Diagnostico del paciente: ', diagnostico['diagnosis'].values[0])


st.subheader('Unidad de cuidado actual:')


st.subheader('Duración de la estancia en la unidad actual:')


st.subheader('Ultima droga recetada:')


st.subheader('Procedimiento realizado al paciente:')
