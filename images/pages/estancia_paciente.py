# Importamos librerias
import streamlit as st
import pandas as pd
import numpy as np
import pymysql

# Agregamos titulo de la página e icono
st.set_page_config(page_title='UCI: Estancia del paciente', page_icon=':hospital:')

# Conexion con ddbb
connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'administrador',
    db = 'pf_uci'
)
cursor = connection.cursor()

# Traemos datos desde la base de datos y guardamos las tablas a usar en datasets.
cursor.execute("select hadm_id, subject_id, admittime, dischtime, admission_type, discharge_location, diagnosis from admissions")
admissions = pd.DataFrame(cursor, columns=("hadm_id", "subject_id", "admittime", "dischtime", "admission_type", "discharge_location", "diagnosis"))

cursor.execute("select subject_id, gender, insurance, marital_status, dob from patients")
patients = pd.DataFrame(cursor, columns=("subject_id", "gender", "insurance", "marital_status", "dob"))

cursor.execute("select hadm_id, drug from prescriptions")
prescriptions = pd.DataFrame(cursor, columns=("hadm_id", "drug"))

cursor.execute("select procedures_icd_id, hadm_id, icd9_code from procedures_icd")
procedures_icd = pd.DataFrame(cursor, columns=("procedures_icd_id", "hadm_id", "icd9_code"))

cursor.execute("select icd9_code, short_title from d_icd_procedures")
d_icd_procedures = pd.DataFrame(cursor, columns=("icd9_code", "short_title"))


st.title('Estancia del paciente')     # Titulo de la app
st.image('images/header.jpg', width=700)


# Input numero de admision / estancia / hospitalización

# Validacion hadm_id ingresado
id_admissions = st.multiselect('***Ingrese numero de admision:***', admissions['hadm_id'], max_selections=1)
if id_admissions == []:
    id_admissions = 142345
    hadm_id = id_admissions
else:
    hadm_id = id_admissions[0]

st.subheader("Datos personales:")
col1, col2 = st.columns(2)
with col1:
    # Nro de paciente
    paciente = admissions.loc[ admissions['hadm_id'] == hadm_id ]
    nro_paciente = paciente['subject_id'].values[0]
    st.write('***Paciente:***', nro_paciente)
with col2:
    # Edad
    edad = admissions[['subject_id','admittime']]
    edad['añoIngreso'] = edad['admittime'].dt.year
    edad = edad.merge(patients[['subject_id','dob']],on='subject_id')
    edad['dob'] = edad['dob'].dt.year
    edad['edad'] = edad['añoIngreso'] - edad['dob']
    edad = edad[['subject_id','edad']]
    edad['edad'][edad['edad'] == 300] = 90
    edad_paciente = edad.loc[ edad['subject_id'] == nro_paciente]
    st.write('***Edad:***', edad_paciente['edad'].values[0])

col1, col2 = st.columns(2)
with col1:
    # Estado civil
    marital_status = patients.loc[ patients['subject_id'] == nro_paciente ]
    st.write('***Estado civil:***', marital_status['marital_status'].values[0])
with col2:
    # Tipo de seguro médico
    insurance = patients.loc[ patients['subject_id'] == nro_paciente ]
    st.write('***Seguro médico:***', insurance['insurance'].values[0])

# Separador
st.markdown('--------------------------------------------------')

st.subheader("Datos de la admisión:")
col1, col2 = st.columns(2)
with col1:
    # Tipo de admision
    tipo_admision = admissions.loc[ admissions['hadm_id'] == hadm_id ]
    st.write('***Tipo de admisión:***', tipo_admision['admission_type'].values[0])
with col2:
    # Diagnostico
    diagnostico = admissions.loc[ admissions['hadm_id'] == hadm_id ]
    st.write('***Diagnóstico del paciente:***', diagnostico['diagnosis'].values[0])

col1, col2 = st.columns(2)
with col1:
    # Unidad de cuidado donde se encuentra
    uci_actual = admissions.loc[ admissions['hadm_id'] == hadm_id ]
    st.write('***UCI donde se encuentra:*** ', uci_actual['discharge_location'].values[0])
with col2:
    # Duración de la estancia del paciente
    lenght_admissions = admissions[['hadm_id', 'subject_id', 'admittime', 'dischtime']]
    lenght_admissions['admittime'] = pd.to_datetime(lenght_admissions['admittime']).dt.date
    lenght_admissions['dischtime'] = pd.to_datetime(lenght_admissions['dischtime']).dt.date
    lenght_admissions['duracion_estadia'] = lenght_admissions['dischtime'] - lenght_admissions['admittime']
    lenght_admissions = lenght_admissions[['hadm_id', 'duracion_estadia']]
    lenght_admissions = lenght_admissions.loc[lenght_admissions['hadm_id'] == hadm_id]
    lenght_admissions['duracion_estadia'] = lenght_admissions['duracion_estadia'].astype('str')
    st.write('***Duración de la estancia:***', lenght_admissions['duracion_estadia'].values[0])

# Separador
st.markdown('--------------------------------------------------')

st.header("Historial de la estancia del paciente:")
col1, col2 = st.columns(2)
with col1:
    # Drogas recetadas al paciente
    prescriptions = prescriptions.loc[prescriptions['hadm_id'] == hadm_id]
    prescriptions = prescriptions[['drug']].sort_values('drug', ascending=True)
    prescriptions = prescriptions['drug'].unique()
    st.write('***:pill: Drogas recetadas***', prescriptions)
with col2:
    # Procedimientos realizados al paciente en la estadia
    procedures = pd.merge(left=procedures_icd, right=d_icd_procedures, left_on='icd9_code', right_on='icd9_code', how='left')
    procedures = procedures.loc[procedures['hadm_id'] == hadm_id]
    procedures = procedures.groupby('short_title', as_index=False).count().sort_values('short_title', ascending=True)
    procedures = procedures['short_title']
    st.write('***:syringe: Procedimientos realizados:***', procedures)