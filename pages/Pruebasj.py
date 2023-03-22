import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
import os

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

# Resto del código permanece igual
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