import pandas as pd
import time
import datetime
from datetime import datetime
admissions = pd.read_csv('PF_UCI-/datasets/ADMISSIONS.csv')
callout = pd.read_csv('PF_UCI-/datasets/CALLOUT.csv')
caregivers = pd.read_csv('PF_UCI-/datasets/CAREGIVERS.csv')
chartevents = pd.read_csv('PF_UCI-/datasets/CHARTEVENTS.csv')
cptevents = pd.read_csv('PF_UCI-/datasets/CPTEVENTS.csv')
datetimeevents = pd.read_csv('PF_UCI-/datasets/DATETIMEEVENTS.csv')
diagnoses_icd = pd.read_csv('PF_UCI-/datasets/DIAGNOSES_ICD.csv')
drgcodes = pd.read_csv('PF_UCI-/datasets/DRGCODES.csv')
d_cpt = pd.read_csv('PF_UCI-/datasets/D_CPT.csv')
d_icd_diagnoses = pd.read_csv('PF_UCI-/datasets/D_ICD_DIAGNOSES.csv')
d_icd_procedures = pd.read_csv('PF_UCI-/datasets/D_ICD_PROCEDURES.csv')
d_items = pd.read_csv('PF_UCI-/datasets/D_ITEMS.csv')
d_labitems = pd.read_csv('PF_UCI-/datasets/D_LABITEMS.csv')

icustays = pd.read_csv('PF_UCI-/datasets/ICUSTAYS.csv')
inputevents_cv = pd.read_csv('PF_UCI-/datasets/INPUTEVENTS_CV.csv')
inputevents_mv = pd.read_csv('PF_UCI-/datasets/INPUTEVENTS_MV.csv')
labevents = pd.read_csv('PF_UCI-/datasets/LABEVENTS.csv')
microbiologyevents = pd.read_csv('PF_UCI-/datasets/MICROBIOLOGYEVENTS.csv')
outputevents = pd.read_csv('PF_UCI-/datasets/OUTPUTEVENTS.csv')
patients = pd.read_csv('PF_UCI-/datasets/PATIENTS.csv')
prescriptions = pd.read_csv('PF_UCI-/datasets/PRESCRIPTIONS.csv')
procedureevents_mv = pd.read_csv('PF_UCI-/datasets/PROCEDUREEVENTS_MV.csv')
procedures_icd = pd.read_csv('PF_UCI-/datasets/PROCEDURES_ICD.csv')
services = pd.read_csv('PF_UCI-/datasets/SERVICES.csv')
transfers = pd.read_csv('PF_UCI-/datasets/TRANSFERS.csv')
# ADMISSIONS
# Eliminar la columna row_id
admissions.drop('row_id', axis=1, inplace=True)
# Reordenar las columnas
admissions = admissions[['hadm_id','subject_id', 'admittime', 'dischtime', 'deathtime',
       'admission_type', 'admission_location', 'discharge_location',
       'insurance', 'language', 'religion', 'marital_status', 'ethnicity',
       'edregtime', 'edouttime', 'diagnosis', 'hospital_expire_flag',
       'has_chartevents_data']]
# Borrar Columnas que se quedarán en la tabla Pacientes
new_admissions=admissions.copy()
new_admissions = new_admissions.drop(['insurance','language', 'religion',
       'marital_status', 'ethnicity'], axis=1)
# PATIENTS
# Eliminar la columna row_id
patients.drop('row_id', axis=1, inplace=True)
# Elimnar filas duplicados en base a los valores de una columna
sd_patients=admissions.copy()                                           # Generamos una copia
sd_patients = sd_patients.drop_duplicates(subset=['subject_id'])        # Borramos duplicados
new_patients = pd.merge(sd_patients, patients, on='subject_id')         # Unión de tablas de pacientes
# Borrar Columnas que se quedarán en la tabla Admisiones
new_patients = new_patients.drop(['admittime', 'dischtime',
       'deathtime', 'admission_type', 'admission_location',
       'discharge_location','edregtime', 'edouttime', 'diagnosis',
       'hospital_expire_flag', 'has_chartevents_data'], axis=1)
# Reordenar Las columnas
new_patients=new_patients[['subject_id','hadm_id', 'insurance', 'language', 'religion',
       'marital_status', 'ethnicity', 'gender', 'dob', 'dod', 'dod_hosp',
       'dod_ssn', 'expire_flag']]
### Reemplazamos la data original de las 2 tablas anteriores
admissions=new_admissions.copy()
patients=new_patients.copy()
# Eliminamos duplicados
admissions.drop_duplicates(inplace = True)
patients.drop_duplicates(inplace = True)
# Cambiamos el tipo de dato de las columnas Fecha
admissions["admittime"] = pd.to_datetime(admissions["admittime"])
admissions["dischtime"] = pd.to_datetime(admissions["dischtime"])
admissions["deathtime"] = pd.to_datetime(admissions["deathtime"])
admissions["edregtime"] = pd.to_datetime(admissions["edregtime"])
admissions["edouttime"] = pd.to_datetime(admissions["edouttime"])
# Cambiamos el tipo de dato de las columnas Fecha
patients['dob'] = pd.to_datetime(patients['dob'])
patients['dod'] = pd.to_datetime(patients['dod'])
patients['dod_hosp'] = pd.to_datetime(patients['dod_hosp'])
patients['dod_ssn'] = pd.to_datetime(patients['dod_ssn'])
# Reemplazaremos el Idioma Faltante con Inglés debido a que el 86% de los completos completos son Inglés
patients['language'] = patients['language'].fillna('N/D')
# Reemplazaremos el dato de religión faltante con "NOT SPECIFIED" debido a que es un dato poco importante
patients['religion'] = patients['religion'].fillna('N/D')
# Reemplazamos el dato de "marital_status" por "UNKNOWN (DEFAULT)" debido a que el dato es desconocido
patients['marital_status'] = patients['marital_status'].fillna('N/D')

# Reordenar las columnas
admissions = admissions[['hadm_id','subject_id', 'admittime', 'dischtime', 'deathtime',
                         'admission_type', 'admission_location', 'discharge_location',
                         'edregtime', 'edouttime', 'diagnosis', 'hospital_expire_flag',
                         'has_chartevents_data']]
# Reordenar Las columnas
patients = patients[ ['subject_id', 'gender', 'insurance', 'language', 'religion',
                             'marital_status', 'ethnicity', 'dob', 'dod', 'dod_hosp',
                             'dod_ssn', 'expire_flag'] ]

# CALLOUT
callout.rename(columns={"row_id":"callout_id"}, inplace=True)
# Eliminamos la columna con el id del paciente
callout.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
callout.drop_duplicates(inplace = True)
# Cambiamos el tipo de dato de la columnas tipo FECHA
callout['createtime'] = pd.to_datetime(callout['createtime'])
callout['updatetime'] = pd.to_datetime(callout['updatetime'])
callout['acknowledgetime'] = pd.to_datetime(callout['acknowledgetime'])
callout['outcometime'] = pd.to_datetime(callout['outcometime'])
callout['firstreservationtime'] = pd.to_datetime(callout['firstreservationtime'])
callout['currentreservationtime'] = pd.to_datetime(callout['currentreservationtime'])
# Lo reemplazaremos con la palabra "UCI" que hace referencia a la unidad general
callout['submit_careunit'] = callout['submit_careunit'].fillna('N/D')
# "discharge_wardid" es La sala a la que fue dada de alta la paciente lo reemplazaremos con la sala más repetida (MODA): 55.0
callout['discharge_wardid'] = callout['discharge_wardid'].fillna(0)

# Reordena columnas para que coincidan con las tablas de sql
callout = callout [['callout_id', 'hadm_id', 'submit_wardid', 'submit_careunit',
                    'curr_wardid', 'curr_careunit', 'callout_wardid', 'callout_service',
                    'request_tele', 'request_resp', 'request_cdiff', 'request_mrsa',
                    'request_vre', 'callout_status', 'callout_outcome', 'discharge_wardid',
                    'acknowledge_status', 'createtime', 'updatetime', 'acknowledgetime',
                    'outcometime', 'firstreservationtime', 'currentreservationtime']]

# Reemplazar las fechas Nulas
callout["firstreservationtime"] = callout["firstreservationtime"].astype("str").replace('NaT',"1970-01-01")
callout["currentreservationtime"] = callout["currentreservationtime"].astype("str").replace('NaT',"1970-01-01")
callout["acknowledgetime"] = callout["acknowledgetime"].astype("str").replace('NaT',"1970-01-01")

# CAREGIVERS
# Renombramos la columna que sera la clave primaria
caregivers.rename(columns={"cgid":"caregivers_id"}, inplace=True) 
# Eliminamos la columna con el id del paciente
caregivers.drop(columns="row_id", inplace=True)
# Eliminamos duplicados
caregivers.drop_duplicates(inplace = True)

#Agregue un nuevo dato a caregivers con el id 0 para cuando se referencie en otra tabla le indique que no hay datos sobre el cuidador que hizo la modificacion
#ESTO PASA EN IMPUTEVENTS_CV, HAY DATOS NULOS EN CUIDADORES Y CONVIERTE LOS DATOS EN TIPO FLOTANTE
nueva_fila = {"caregivers_id":0, "label":"N/A", "description":"No Data"}
nuevo = pd.DataFrame(data=nueva_fila, index=[0])
caregivers = pd.concat([caregivers,nuevo], axis = 0, join = "outer", ignore_index=True)
#Los datos nulos en etiqueta se cambiaron por "No Data"
caregivers["label"].fillna("N/D",inplace=True)
caregivers["description"].fillna("N/D",inplace=True)
# "label" es Etiqueta que identifica al cuidador del paciente y lo reemplazaremos por la "Not Exist"
caregivers['label'] = caregivers['label'].fillna('N/D')
# "description" es la descripción más detallada del cuidador y lo reemplazaremos con la "Not Exist"
caregivers['description'] = caregivers['description'].fillna('N/D')
# Reordena las columnas para que coincidan con las tablas de sql
caregivers = caregivers[ ['caregivers_id', 'label', 'description'] ]
# CHARTEVENTS
# Renombramos la columna que sera la clave primaria
chartevents.rename(columns={"row_id":"chartevents_id"}, inplace=True)
# Eliminamos la columna con el id del paciente
chartevents.drop(columns="subject_id", inplace=True)
# Eliminamos duplicados
chartevents.drop_duplicates(inplace = True)
#Fechas a tipo datetime
chartevents["charttime"] = pd.to_datetime(chartevents["charttime"])
chartevents["storetime"] = pd.to_datetime(chartevents["storetime"])

#Normalizacion del valor ml por mL
unidad = chartevents["valueuom"] == "ml"
chartevents.loc[unidad,["valueuom"]] = "mL"
#Remplazar los valores nulos por 0 para pasar el tipo de dato a entero, aplique o no el 0 representara lo mismo
chartevents["warning"].fillna(0, inplace=True)
chartevents["warning"] = chartevents["warning"].astype("int64")
chartevents["error"].fillna(0, inplace=True)
chartevents["error"] = chartevents["error"].astype("int64")
#Tambien se agrego un 0 en los campos de icustay_id, esto representa que no hay data sobre el icustay
chartevents["icustay_id"].fillna(0, inplace=True)
chartevents["icustay_id"] = chartevents["icustay_id"].astype("int64")

#Datos rellenados
chartevents["value"].fillna("N/D", inplace=True)
chartevents["resultstatus"].fillna("N/D", inplace=True)
chartevents["stopped"].fillna("N/D", inplace=True)
chartevents["valuenum"].fillna(0, inplace=True)

# Reordena las columnas para que coincidan con las tablas de sql
chartevents = chartevents[ ['chartevents_id', 'hadm_id', 'icustay_id', 'itemid', 'charttime',
                            'storetime', 'cgid', 'value', 'valuenum', 'valueuom', 'warning',
                            'error', 'resultstatus', 'stopped'] ]

chartevents["valueuom"] = chartevents["valueuom"].astype("str").replace('NaT',"1970-01-01")
# CPTEVENTS
# Renombramos la columna que sera la clave primaria
cptevents.rename(columns={'row_id' : 'cptevents_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
cptevents.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
cptevents.drop_duplicates(inplace = True)

# En la columna ticket_id_seq son datos decimales pero ninguno tiene una decima diferente de 0 por lo que supongo que son valores enteros
# Que por los valores faltantes de esta columna se convirtieron en tipo flotantes
#Se remplazaron los valores que faltan por 0, con este cambio los tickets con identificacion de 0 significaran que no aplica el ticket
cptevents["ticket_id_seq"].fillna(0,inplace=True)
cptevents["ticket_id_seq"] = cptevents["ticket_id_seq"].astype("int64")

#Fechas a tipo datetime
cptevents["chartdate"] = pd.to_datetime(cptevents["chartdate"])

#datos rellenados
cptevents["cpt_suffix"].fillna(0,inplace=True)
cptevents["description"].fillna("N/D",inplace=True)

# Reordena las columnas para que coincidan con las tablas de sql
cptevents = cptevents[ ['cptevents_id', 'hadm_id', 'costcenter', 'chartdate', 'cpt_cd',
                        'cpt_number', 'cpt_suffix', 'ticket_id_seq', 'sectionheader',
                        'subsectionheader', 'description'] ]

cptevents["chartdate"] = cptevents["chartdate"].astype("str").replace('NaT',"1970-01-01")
# DATETIMEEVENTS
# Renombramos la columna que sera la clave primaria
datetimeevents.rename(columns={'row_id':'datetimeevents_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
datetimeevents.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
datetimeevents.drop_duplicates(inplace = True)

#Fechas a datetime
datetimeevents["charttime"] = pd.to_datetime(datetimeevents["charttime"])
datetimeevents["storetime"] = pd.to_datetime(datetimeevents["storetime"])
datetimeevents["value"] = pd.to_datetime(datetimeevents["value"])

#Los valores nulos fueron remplazados con cero, ahora aplique o no significara lo mismo
datetimeevents["warning"].fillna(0,inplace=True)
datetimeevents["warning"] = datetimeevents["warning"].astype("int64")
datetimeevents["error"].fillna(0,inplace=True)
datetimeevents["error"] = datetimeevents["error"].astype("int64")
#Se remplazaron los valores faltantes por 0 para convertir el tipo de dato a entero
datetimeevents["icustay_id"].fillna(0,inplace=True)
datetimeevents["icustay_id"] = datetimeevents["icustay_id"].astype("int64")

#datos rellenados
datetimeevents["resultstatus"].fillna(0, inplace=True)
datetimeevents["stopped"].fillna("N/D", inplace=True)

# Reordena las columnas para que coincidan con las tablas de sql
datetimeevents = datetimeevents[ ['datetimeevents_id', 'hadm_id', 'icustay_id', 'itemid', 'charttime',
                                  'storetime', 'cgid', 'value', 'valueuom', 'warning', 'error',
                                  'resultstatus', 'stopped'] ]

datetimeevents["value"] = datetimeevents["value"].astype("str").replace('NaT',"1970-01-01")
# DIAGNOSES_ICD
# Renombramos la columna que sera la clave primaria
diagnoses_icd.rename(columns ={'row_id' : 'diagnoses_icd_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
diagnoses_icd.drop(columns = ['subject_id'], inplace = True)
# Acomodamos tipos de datos
diagnoses_icd['hadm_id'] = diagnoses_icd['hadm_id'].astype(int)
diagnoses_icd['seq_num'] = diagnoses_icd['seq_num'].astype(int)
diagnoses_icd['diagnoses_icd_id'] = diagnoses_icd['diagnoses_icd_id'].astype(int)
# Eliminamos duplicados
diagnoses_icd.drop_duplicates(inplace = True)
# Reordena las columnas para que coincidan con las tablas de sql
diagnoses_icd = diagnoses_icd[ ['diagnoses_icd_id', 'hadm_id', 'seq_num', 'icd9_code'] ]
# DRGCODES
# Renombramos la columna que sera la clave primaria
drgcodes.rename(columns ={'row_id' : 'drgcodes_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
drgcodes.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
drgcodes.drop_duplicates(inplace = True)
#datos rellenados
drgcodes["drg_severity"].fillna(0, inplace=True)
drgcodes["drg_mortality"].fillna(0, inplace=True)
# Reordena las columnas para que coincidan con las tablas de sql
drgcodes = drgcodes[ ['drgcodes_id', 'hadm_id', 'drg_type', 'drg_code',
                      'description', 'drg_severity', 'drg_mortality'] ]
# D_CPT
# Renombramos la columna que sera la clave primaria
d_cpt.rename(columns ={'row_id' : 'd_cpt_id'}, inplace = True)
# Eliminamos duplicados
d_cpt.drop_duplicates(inplace = True)
# Rellenamos valores faltantes
d_cpt["codesuffix"].fillna('N/D', inplace=True)
# Reordena las columnas para que coincidan con las tablas de sql
d_cpt = d_cpt[ ['d_cpt_id', 'category', 'sectionrange', 'sectionheader',
                'subsectionrange', 'subsectionheader', 'codesuffix',
                'mincodeinsubsection', 'maxcodeinsubsection'] ]
# D_ICD_DIAGNOSES
# Eliminamos la columna con el id del paciente
d_icd_diagnoses.drop(columns = ['row_id'], inplace = True)
# Eliminamos duplicados
d_icd_diagnoses.drop_duplicates(inplace = True)
# Reordena las columnas para que coincidan con las tablas de sql
d_icd_diagnoses = d_icd_diagnoses[ ['icd9_code', 'short_title', 'long_title'] ]
# D_ICD_PROCEDURES
# Eliminamos la columna con el id del paciente
d_icd_procedures.drop(columns = ['row_id'], inplace = True)
# Eliminamos duplicados
d_icd_procedures.drop_duplicates(inplace = True)
# Reordena las columnas para que coincidan con las tablas de sql
d_icd_procedures = d_icd_procedures[ ['icd9_code', 'short_title', 'long_title'] ]
# D_ITEMS
# Renombramos la columna que sera la clave primaria
d_items.rename(columns ={'itemid' : 'item_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
d_items.drop(columns = ['row_id'], inplace = True)
# Eliminamos duplicados
d_items.drop_duplicates(inplace = True)
# Reemplazamos valores nulos
d_items["label"].fillna('N/D', inplace=True)
d_items["abbreviation"].fillna('N/D', inplace=True)
d_items["category"].fillna('N/D', inplace=True)
d_items["unitname"].fillna('N/D', inplace=True)
d_items["param_type"].fillna('N/D', inplace=True)
d_items["conceptid"].fillna(0, inplace=True)
# Reordena las columnas para que coincida con las tablas sql
d_items = d_items[ ['item_id', 'label', 'abbreviation', 'dbsource', 'linksto',
                    'category', 'unitname', 'param_type', 'conceptid'] ]
# D_LABITEMS
# Renombramos la columna que sera la clave primaria
d_labitems.rename(columns ={'itemid' : 'item_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
d_labitems.drop(columns = ['row_id'], inplace = True)
# Eliminamos duplicados
d_labitems.drop_duplicates(inplace = True)
# Reemplazamos valores faltantes
d_labitems["loinc_code"].fillna('N/D', inplace=True)
# Reordena las columnas para que coincida con las tablas sql
d_labitems = d_labitems[ ['item_id', 'label', 'fluid', 'category', 'loinc_code'] ]
# ICUSTAYS
# Eliminamos la columna con el id del paciente
icustays.drop(columns = ['subject_id'], inplace = True)
# Eliminamos la columna con el id del paciente
icustays.drop(columns = ['row_id'], inplace = True)
# Eliminamos duplicados
icustays.drop_duplicates(inplace = True)
icustays["intime"] = pd.to_datetime(icustays["intime"])
icustays["outtime"] = pd.to_datetime(icustays["outtime"])
# Reordenamos los campos para que coincidan con las tablas de sql
icustays = icustays[ ['icustay_id', 'hadm_id', 'dbsource', 'first_careunit', 'last_careunit', 'first_wardid', 'last_wardid', 'intime', 'outtime', 'los'] ]
# INPUTEVENTS_CV
# Renombramos la columna que sera la clave primaria
inputevents_cv.rename(columns={'row_id' : 'inputevents_cv_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
inputevents_cv.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
inputevents_cv.drop_duplicates(inplace = True)

# Normalizacion de los datos "ml" a "mL"
unidad = inputevents_cv["amountuom"] == "ml"
inputevents_cv.loc[unidad,["amountuom"]] = "mL"
unidad = inputevents_cv["originalamountuom"] == "ml"
inputevents_cv.loc[unidad,["originalamountuom"]] = "mL"
# Lo mismo pero para unidades vectoriales
unidad = inputevents_cv["originalrateuom"] == 'ml/hr'
inputevents_cv.loc[unidad,["originalrateuom"]] = "mL/hr"

# Normalizando los valores del campo "newbottle" para cambiar el tipo de dato de float a integer
inputevents_cv["newbottle"].fillna(0, inplace=True)
inputevents_cv["newbottle"] = inputevents_cv["newbottle"].astype("int64") #0 representa que no se uso un nuevo bote independientemente de si uso alguno o no ("incluir en la documentacion")

#Fechas a tipo datetime
inputevents_cv["charttime"] = pd.to_datetime(inputevents_cv["charttime"])
inputevents_cv["storetime"] = pd.to_datetime(inputevents_cv["storetime"])

#Los valores nulos de este campo se remplazan por cero para cambiar el tipo de dato
# OJO ATENCHION XD SE DEBE DE AGREGAR EL VALOR 0 A LA TABLA DE CGID E INDICAR QUE NO REPRESENTA A NADIE O SIMPLEMENTE ESPECIFICARLO DIRECTAMENTE EN LA DOCUMENTACION
inputevents_cv["cgid"].fillna(0,inplace=True)
inputevents_cv["cgid"] = inputevents_cv["cgid"].astype("int64")

# Reordenamos los campos para que coincidan con las tablas de sql
inputevents_cv = inputevents_cv[ [ 'inputevents_cv_id', 'hadm_id', 'icustay_id', 'charttime', 'itemid',
                                   'amount', 'amountuom', 'rate', 'rateuom', 'storetime', 'cgid',
                                   'orderid', 'linkorderid', 'stopped', 'newbottle', 'originalamount',
                                   'originalamountuom', 'originalroute', 'originalrate', 'originalrateuom',
                                   'originalsite'] ]

inputevents_cv['rate'].fillna(0, inplace=True)  # Completamos con 0 los valores nulos
inputevents_cv['originalamount'].fillna(0, inplace=True)  # Completamos con 0 los valores nulos
inputevents_cv['originalrate'].fillna(0, inplace=True)  # Completamos con 0 los valores nulos
inputevents_cv['amount'].fillna(0, inplace=True)  # Completamos con 0 los valores nulos
inputevents_cv['rateuom'].fillna("N/D", inplace=True)
inputevents_cv['amountuom'].fillna("N/D", inplace=True)
inputevents_cv['originalamountuom'].fillna("N/D", inplace=True)
inputevents_cv['originalroute'].fillna("N/D", inplace=True)
inputevents_cv['originalrateuom'].fillna("N/D", inplace=True)
inputevents_cv['originalsite'].fillna("N/D", inplace=True)
inputevents_cv['stopped'].fillna("N/D", inplace=True)
# INPUTEVENTS_MV
# Renombramos la columna que sera la clave primaria
inputevents_mv.rename(columns={'row_id' : 'inputevents_mv_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
inputevents_mv.drop(columns = ['subject_id'], inplace = True)
# Normalizacion de mililitros
unidad = inputevents_mv["totalamountuom"] == "ml"
inputevents_mv.loc[unidad,["totalamountuom"]] = "mL"
unidad1 = inputevents_mv["amountuom"] == "ml"
inputevents_mv.loc[unidad1,["amountuom"]] = "mL"
# Valores negativos
outliers = inputevents_mv["amount"] < 0
inputevents_mv["cambioend"] = inputevents_mv["endtime"] #Crear una nueva columna temporal para reorganizar las fechas
inputevents_mv.loc[outliers,["endtime"]] = inputevents_mv["starttime"]  #Reorganizar las fechas en donde el valor es negativo
inputevents_mv.loc[outliers,["starttime"]] = inputevents_mv["cambioend"]
inputevents_mv.drop("cambioend", axis=1, inplace=True) #Eliminar la columna temporal
inputevents_mv.loc[outliers,["amount"]] = inputevents_mv["amount"] * -1 #Multiplicar por -1 para eliminar el signo
# Eliminamos duplicados
inputevents_mv.drop_duplicates(inplace = True)

#Fechas a tipo datetime
inputevents_mv["starttime"] = pd.to_datetime(inputevents_mv["starttime"])
inputevents_mv["endtime"] = pd.to_datetime(inputevents_mv["endtime"])
inputevents_mv["comments_date"] = pd.to_datetime(inputevents_mv["comments_date"])
inputevents_mv["storetime"] = pd.to_datetime(inputevents_mv["storetime"])

#datos rellenados
inputevents_mv["rateuom"].fillna("N/D", inplace=True)
inputevents_mv["secondaryordercategoryname"].fillna("N/D", inplace=True)
inputevents_mv["totalamountuom"].fillna("N/D", inplace=True)
inputevents_mv["comments_editedby"].fillna("N/D", inplace=True)
inputevents_mv["comments_canceledby"].fillna("N/D", inplace=True)

inputevents_mv["rate"].fillna(0, inplace=True)
inputevents_mv["totalamount"].fillna(0, inplace=True)
inputevents_mv["rate"].fillna(0, inplace=True)
inputevents_mv["comments_date"].fillna("1970-01-01", inplace=True)
# Reordenamos los campos para que coincidan con las tablas de sql
inputevents_mv = inputevents_mv[ ['inputevents_mv_id', 'hadm_id', 'icustay_id', 'starttime', 'endtime',
                                  'itemid', 'amount', 'amountuom', 'rate', 'rateuom', 'storetime', 'cgid',
                                  'orderid', 'linkorderid', 'ordercategoryname', 'secondaryordercategoryname',
                                  'ordercomponenttypedescription', 'ordercategorydescription', 'patientweight',
                                  'totalamount', 'totalamountuom', 'isopenbag', 'continueinnextdept', 
                                  'cancelreason', 'statusdescription', 'comments_editedby', 'comments_canceledby',
                                  'comments_date', 'originalamount', 'originalrate'] ]
# LABEVENTS
# Renombramos la columna que sera la clave primaria
labevents.rename(columns ={'row_id' : 'labevents_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
labevents.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
labevents.drop_duplicates(inplace = True)
labevents["charttime"] = pd.to_datetime(labevents["charttime"])
# Rellenamos datos faltantes
labevents["value"].fillna('N/D', inplace=True)
labevents["valuenum"].fillna(0, inplace=True)
labevents["flag"].fillna('N/D', inplace=True)
labevents["hadm_id"].fillna(0, inplace=True)
# Cambiamos tipo de dato que no se porque esta en float
labevents["hadm_id"] = labevents["hadm_id"].astype(int)
labevents["valueuom"].fillna('N/D', inplace=True)
# Reordenamos los campos para que coincidan con las tablas de sql
labevents = labevents[ ['labevents_id', 'hadm_id', 'itemid', 'charttime',
                        'value', 'valuenum', 'valueuom', 'flag'] ]
# MICROBIOLOGYEVENTS
# Renombramos la columna que sera la clave primaria
microbiologyevents.rename(columns ={'row_id' : 'microbiologyevents_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
microbiologyevents.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
microbiologyevents.drop_duplicates(inplace = True)
microbiologyevents["chartdate"] = pd.to_datetime(microbiologyevents["chartdate"])
microbiologyevents["charttime"] = pd.to_datetime(microbiologyevents["charttime"])
# Rellenamos datos faltantes
microbiologyevents["org_itemid"].fillna(0, inplace=True)
microbiologyevents["org_name"].fillna('N/D', inplace=True)
microbiologyevents["isolate_num"].fillna(0, inplace=True)
microbiologyevents["ab_itemid"].fillna(0, inplace=True)
microbiologyevents["ab_name"].fillna('N/D', inplace=True)
microbiologyevents["dilution_text"].fillna('N/D', inplace=True)
microbiologyevents["dilution_comparison"].fillna('N/D', inplace=True)
microbiologyevents["dilution_value"].fillna(0, inplace=True)
microbiologyevents["interpretation"].fillna('N/D', inplace=True)
microbiologyevents["charttime"].fillna('1970-01-01', inplace=True)
# Reordenamos los campos para que coincidan con las tablas de sql
microbiologyevents = microbiologyevents[ ['microbiologyevents_id', 'hadm_id', 'chartdate', 'charttime',
                                          'spec_itemid', 'spec_type_desc', 'org_itemid', 'org_name',
                                          'isolate_num', 'ab_itemid', 'ab_name', 'dilution_text',
                                          'dilution_comparison', 'dilution_value', 'interpretation'] ]
# OUTPUTEVENTS
# Renombramos la columna que sera la clave primaria
outputevents.rename(columns={'row_id' : 'outputevents_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
outputevents.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
outputevents.drop_duplicates(inplace = True)

#Fechas a tipo datetime
outputevents["charttime"] = pd.to_datetime(outputevents["charttime"])

#Noremalizacion de los valores "ml" a "mL"
unidad = outputevents["valueuom"] == "ml"
outputevents.loc[unidad,["valueuom"]] = "mL"

#datos rellenados
outputevents["stopped"].fillna(0, inplace=True)
outputevents["newbottle"].fillna(0, inplace=True)
outputevents["iserror"].fillna(0, inplace=True)
outputevents["value"].fillna(0, inplace=True)
outputevents["valueuom"].fillna("N/D", inplace=True)
outputevents["icustay_id"].fillna(0, inplace=True)
# Hay un valor en el campo icustay faltante, como es solo uno lo busque manualmente y en la base de datos
# Puede especificarce que no admita nulos en SQL para que no vuelva a pasar este problema.
#outputevents[outputevents["icustay_id"].isna()] 
#icustays[icustays["hadm_id"] == 163189] # Buscamos el valor que nos dio en la visualizacion de arriba
#outputevents.loc[7939,"icustay_id"] = 239396 # aqui es donde ago la modificacion, (Pueden borrase las lineas de arriba ya que esta es la que hace el cambio)
#outputevents["icustay_id"] = outputevents["icustay_id"].astype("int64") # Se hace el cambio de tipo de dato a int64 para que coincida con las demas tablas
# Reordenamos los campos para que coincidan con las tablas de sql
outputevents = outputevents[ ['outputevents_id', 'hadm_id', 'icustay_id', 'charttime', 'itemid', 'value',
                              'valueuom', 'storetime', 'cgid', 'stopped', 'newbottle', 'iserror'] ]
# PRESCRIPTIONS
# Renombramos la columna que sera la clave primaria
prescriptions.rename(columns ={'row_id' : 'prescriptions_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
prescriptions.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
prescriptions.drop_duplicates(inplace = True)
prescriptions["startdate"] = pd.to_datetime(prescriptions["startdate"]).astype("str").replace('NaT',"1970-01-01")
prescriptions["enddate"] = pd.to_datetime(prescriptions["enddate"]).astype("str").replace('NaT',"1970-01-01")
# Rellenamos valores faltantes
prescriptions["icustay_id"].fillna(0, inplace=True)
prescriptions["drug_name_poe"].fillna('N/D', inplace=True)
prescriptions["drug_name_generic"].fillna('N/D', inplace=True)
prescriptions["formulary_drug_cd"].fillna('N/D', inplace=True)
prescriptions["gsn"].fillna(0, inplace=True)
prescriptions["ndc"].fillna(0, inplace=True)
prescriptions["form_unit_disp"].fillna('N/D', inplace=True)
prescriptions["enddate"].fillna('', inplace=True)
prescriptions["enddate"].replace('Nat','Null')
# Reordenamos los campos para que coincidan con las tablas de sql
prescriptions = prescriptions[ ['prescriptions_id', 'hadm_id', 'icustay_id', 'startdate', 'enddate',
                                'drug_type', 'drug', 'drug_name_poe', 'drug_name_generic',
                                'formulary_drug_cd', 'gsn', 'ndc', 'prod_strength', 'dose_val_rx',
                                'dose_unit_rx', 'form_val_disp', 'form_unit_disp', 'route'] ]
# PROCEDUREEVENTS_MV
# Renombramos la columna que sera la clave primaria
procedureevents_mv.rename(columns={'row_id' : 'procedureevents_mv_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
procedureevents_mv.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
procedureevents_mv.drop_duplicates(inplace = True)

#Fechas a tipo datetime
procedureevents_mv["starttime"] = pd.to_datetime(procedureevents_mv["starttime"])
procedureevents_mv["endtime"] = pd.to_datetime(procedureevents_mv["endtime"])
procedureevents_mv["comments_date"] = pd.to_datetime(procedureevents_mv["comments_date"])
procedureevents_mv["storetime"] = pd.to_datetime(procedureevents_mv["storetime"])

#datos rellenados
procedureevents_mv["location"].fillna("N/D", inplace=True)
procedureevents_mv["secondaryordercategoryname"] = procedureevents_mv["secondaryordercategoryname"].astype(str)
procedureevents_mv["secondaryordercategoryname"].fillna("N/D", inplace=True)
procedureevents_mv["locationcategory"].fillna("N/D", inplace=True)
procedureevents_mv["comments_editedby"].fillna("N/D", inplace=True)
procedureevents_mv["comments_canceledby"].fillna("N/D", inplace=True)
procedureevents_mv["comments_date"].fillna("1970-01-01", inplace=True)
# Reordenamos los campos para que coincidan con las tablas de sql
procedureevents_mv = procedureevents_mv[ ['procedureevents_mv_id', 'hadm_id', 'icustay_id', 'starttime', 'endtime',
                                          'itemid', 'value', 'valueuom', 'location', 'locationcategory',
                                          'storetime', 'cgid', 'orderid', 'linkorderid', 'ordercategoryname',
                                          'secondaryordercategoryname', 'ordercategorydescription', 'isopenbag',
                                          'continueinnextdept', 'cancelreason', 'statusdescription',
                                          'comments_editedby', 'comments_canceledby', 'comments_date'] ]
# PROCEDURES_ICD
# Renombramos la columna que sera la clave primaria
procedures_icd.rename(columns ={'row_id' : 'procedures_icd_id'}, inplace = True)
# Eliminamos la columna con el id del paciente
procedures_icd.drop(columns = ['subject_id'], inplace = True)
# Corregimos tipos de dato
procedures_icd['hadm_id'] = procedures_icd['hadm_id'].astype(int)
procedures_icd['seq_num'] = procedures_icd['seq_num'].astype(int)
procedures_icd['procedures_icd_id'] = procedures_icd['procedures_icd_id'].astype(int)
# Eliminamos duplicados
procedures_icd.drop_duplicates(inplace = True)
# Reordenamos los campos para que coincidan con las tablas de sql
procedures_icd = procedures_icd[ ['procedures_icd_id', 'hadm_id', 'seq_num', 'icd9_code'] ]
# SERVICES
# Renombrar PK
services.rename(columns={"row_id":"services_id"}, inplace=True)
# Eliminamos la columna con el id del paciente
services.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
services.drop_duplicates(inplace = True)
# Cambiamos el tipo de dato de la columnas tipo FECHA
services['transfertime'] = pd.to_datetime(services['transfertime'])
# Debido a que no existe ese servicio anterior
services['prev_service'] = services['prev_service'].fillna('N/D')
# Reordenamos los campos para que coincidan con las tablas de sql
services = services[ ['services_id', 'hadm_id', 'transfertime', 'prev_service', 'curr_service'] ]
# TRANSFERS
# Renombrar PK
transfers.rename(columns={"row_id":"transfers_id"}, inplace=True)
# Eliminamos la columna con el id del paciente
transfers.drop(columns = ['subject_id'], inplace = True)
# Eliminamos duplicados
transfers.drop_duplicates(inplace = True)
# Cambiamos el tipo de dato de la columnas tipo FECHA
transfers['intime'] = pd.to_datetime(transfers['intime'])
transfers['outtime'] = pd.to_datetime(transfers['outtime'])
# La ausencia lo reemplazaremos con 0
transfers['icustay_id'] = transfers['icustay_id'].fillna(0)
# Hace referencia a la sala previa donde se econtraba el paciente
# Al igual que 'submit_careunit' el valor lo reeplazaremos con el valor genérico N/D que hace referencia general a la unidad
transfers['prev_careunit'] = transfers['prev_careunit'].fillna('N/D')
# Si actualmente se encuentra en una unidad de cuidados, el tipo de N/D se indica aquí "curr_careunit"
# Reemplzaremos con el valor genérico "UCI"
transfers['curr_careunit'] = transfers['curr_careunit'].fillna('N/D')
# "prev_wardid" es Identificador de la *sala* previa del paciente. Lo Completaremos con 0
transfers['prev_wardid'] = transfers['prev_wardid'].fillna(0)
# "curr_wardid" es Identificador de la *sala* previa del paciente. Lo Completaremos con 0
transfers['curr_wardid'] = transfers['curr_wardid'].fillna(0)
# "los" es Duración de la estancia en la UCI en minutos y al no existir lo reemplazaremos con 0
transfers['los'] = transfers['los'].fillna(0)
transfers['outtime'].fillna('1970-01-01',inplace= True)
# Reordenamos los campos para que coincidan con las tablas de sql
transfers = transfers[ ['transfers_id', 'hadm_id', 'icustay_id', 'dbsource',
                        'eventtype', 'prev_careunit', 'curr_careunit', 'prev_wardid',
                        'curr_wardid', 'intime', 'outtime', 'los'] ]
# ___________________________________________________________
# CARGA A SQL
import pymysql
connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '12345678',
    db = 'pf_uci'
  )
cursor = connection.cursor()
# Creación de la tabla auditoría
data_auditoria = {'fecha_creacion': [],'name_table': [], 'quantity_rows_original': [],'quantity_rows_sql': [], 'time_load': [], 'estado': []}
auditoria = pd.DataFrame(data_auditoria)
# ADMISSIONS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table admissions"
cursor.execute(sql)
connection.commit()
# Cargamos los datos al sistema
for i in range(len(admissions)):
    texto = admissions.iloc[i].to_list()
    sql ="INSERT INTO admissions VALUES(" + str(texto).strip("[]").replace('NaT', "NULL") + ")"
    cursor.execute(sql)
connection.commit()
end_time = time.time()
# name_table
name_table='admissions'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=admissions.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# CALLOUT
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table callout"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = callout.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO callout VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='callout'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=callout.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# CAREGIVERS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table caregivers"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = caregivers.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO caregivers VALUES (%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='caregivers'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=caregivers.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# CHARTEVENTS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table chartevents"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = chartevents.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO chartevents VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='chartevents'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=chartevents.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# CPTEVENTS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table cptevents"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = cptevents.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO cptevents VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='cptevents'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=cptevents.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# DATETIMEEVENTS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table datetimeevents"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = datetimeevents.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO datetimeevents VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='datetimeevents'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=datetimeevents.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# DIAGNOSES_ICD
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table diagnoses_icd"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = diagnoses_icd.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO diagnoses_icd VALUES (%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='diagnoses_icd'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=diagnoses_icd.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# DRGCODES
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table drgcodes"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = drgcodes.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO drgcodes VALUES (%s,%s,%s,%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='drgcodes'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=drgcodes.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# D_CPT
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table d_cpt"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = d_cpt.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO d_cpt VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='d_cpt'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=d_cpt.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# D_ICD_DIAGNOSES
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table d_icd_diagnoses"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = d_icd_diagnoses.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO d_icd_diagnoses VALUES (%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='d_icd_diagnoses'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=d_icd_diagnoses.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# D_ICD_PROCEDURES
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table d_icd_procedures"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = d_icd_procedures.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO d_icd_procedures VALUES (%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='d_icd_procedures'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=d_icd_procedures.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# D_ITEMS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table d_items"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = d_items.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO d_items VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='d_items'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=d_items.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# D_LABITEMS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table d_labitems"
cursor.execute(sql)
connection.commit()
# Crea una lista de los valores de la Tabla
chart = d_labitems.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO d_labitems VALUES (%s,%s,%s,%s,%s)""",chart)
connection.commit()
end_time = time.time()
# name_table
name_table='d_labitems'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=d_labitems.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# ICUSTAYS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table icustays"
cursor.execute(sql)
connection.commit()

icu = icustays.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO icustays VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",icu)

connection.commit()
end_time = time.time()
# name_table
name_table='icustays'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=icustays.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# INPUTEVENTS_CV
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table inputevents_cv"
cursor.execute(sql)
connection.commit()

in_cv = inputevents_cv.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO inputevents_cv VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",in_cv)

connection.commit()
end_time = time.time()
# name_table
name_table='inputevents_cv'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=inputevents_cv.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# INPUTEVENTS_MV
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table inputevents_mv"
cursor.execute(sql)
connection.commit()

in_mv = inputevents_mv.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO inputevents_mv VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",in_mv)

connection.commit()
end_time = time.time()
# name_table
name_table='inputevents_mv'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=inputevents_mv.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# LABEVENTS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table labevents"
cursor.execute(sql)
connection.commit()

l_eve = labevents.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO labevents VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",l_eve)

connection.commit()
end_time = time.time()
# name_table
name_table='labevents'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=labevents.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# MICROBIOLOGYEVENTS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table microbiologyevents"
cursor.execute(sql)
connection.commit()

micro = microbiologyevents.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO microbiologyevents VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",micro)

connection.commit()
end_time = time.time()
# name_table
name_table='microbiologyevents'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=microbiologyevents.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# OUTPUTEVENTS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table outputevents"
cursor.execute(sql)
connection.commit()

outp = outputevents.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO outputevents VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",outp)

connection.commit()
end_time = time.time()
# name_table
name_table='outputevents'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=outputevents.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# PATIENTS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table patients"
cursor.execute(sql)
connection.commit()

# eliminar primary key de sql porque toma valores repetidos cuando no los hay
for i in range(len(patients)):
    texto = patients.iloc[i].to_list()
    sql ="INSERT INTO patients VALUES(" + str(texto).strip("[]").replace('NaT', "NULL") + ")"
    cursor.execute(sql)

connection.commit()
end_time = time.time()
# name_table
name_table='patients'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=patients.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# PRESCRIPTIONS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table prescriptions"
cursor.execute(sql)
connection.commit()

presc = prescriptions.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO prescriptions VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",presc)
connection.commit()
end_time = time.time()
# name_table
name_table='prescriptions'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=prescriptions.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# PROCEDUREEVENTS_MV
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table procedureevents_mv"
cursor.execute(sql)
connection.commit()

pro_ev = procedureevents_mv.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO procedureevents_mv VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",pro_ev)

connection.commit()
end_time = time.time()
# name_table
name_table='procedureevents_mv'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=procedureevents_mv.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# PROCEDURES_ICD
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table procedures_icd"
cursor.execute(sql)
connection.commit()

pro_icd = procedures_icd.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO procedures_icd VALUES (%s,%s,%s,%s)""",pro_icd)

connection.commit()
end_time = time.time()
# name_table
name_table='procedures_icd'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=procedures_icd.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# SERVICES
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table services"
cursor.execute(sql)
connection.commit()

serv = services.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO services VALUES (%s,%s,%s,%s,%s)""",serv)

connection.commit()
end_time = time.time()
# name_table
name_table='services'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=services.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# TRANSFERS
start_time = time.time()
# Tuncar las tablas para no perder la configuración
cursor = connection.cursor()
sql ="truncate table transfers"
cursor.execute(sql)
connection.commit()

tran = transfers.values.tolist()
cursor = connection.cursor()
cursor.executemany("""INSERT INTO transfers VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",tran)

connection.commit()
end_time = time.time()
# name_table
name_table='transfers'                                # CAMBIAR NOMBRE DE TABLA
#quantity_rows_original
quantity_rows_original=transfers.shape[0]              # CAMBIAR NOMBRE DE TABLA
#___________________________________________________________
# time
fecha_creacion = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
fecha_creacion = str(fecha_creacion)
#quantity_rows_sql
cursor = connection.cursor()
sql ="SELECT COUNT(*) FROM "+name_table+""""""
cursor.execute(sql)
result = cursor.fetchone()
quantity_rows_sql=result[0]
connection.commit()
#time_load
time_load= round(int(end_time - start_time))
# Estado
if quantity_rows_original==quantity_rows_sql:
    estado='Carga Normal'
else:
    estado='Carga incompleta'
# Ingesta de resultados de auditoria
new_audit = {'fecha_creacion': fecha_creacion, 'name_table': name_table, 'quantity_rows_original': quantity_rows_original, 'quantity_rows_sql': quantity_rows_sql, 'time_load': time_load, 'estado': estado }
# add the new row to the DataFrame
auditoria = auditoria.append(new_audit, ignore_index=True)
# CARGA DE AUDITORIAS
# Cambio de tipo de dato
#auditoria['fecha_creacion'] = pd.to_datetime(auditoria['fecha_creacion'])
auditoria['fecha_str'] = auditoria['fecha_creacion'].astype("str")
auditoria['fecha_str'] = auditoria['fecha_str'].str.replace('-', '').str.replace(' ', '').str.replace(':', '')
# Concatenar la cadena de fecha y el número de fila
auditoria['id_auditoria'] =auditoria['fecha_str'] + auditoria.index.astype(str)
# Eliminar la columna 'fecha_str' si no es necesaria
auditoria.drop('fecha_str', axis=1, inplace=True)
# Cambio de Tipo de variables
auditoria["name_table"] = auditoria["name_table"].astype("str")
auditoria["quantity_rows_original"] = auditoria["quantity_rows_original"].astype("int")
auditoria["quantity_rows_sql"] = auditoria["quantity_rows_sql"].astype("int")
auditoria["time_load"] = auditoria["time_load"].astype("int")
auditoria["estado"] = auditoria["estado"].astype("str")
auditoria['fecha_creacion'] = pd.to_datetime(auditoria['fecha_creacion'])
auditoria["fecha_creacion"] = auditoria["fecha_creacion"].astype("str")
auditoria["id_auditoria"] = auditoria["id_auditoria"].astype("str")
#Reordenar columnas
auditoria = auditoria[ ['id_auditoria', 'fecha_creacion', 'name_table', 'quantity_rows_original',
                        'quantity_rows_sql', 'time_load', 'estado'] ]
# Creación de Lista
chart = auditoria.values.tolist()
# Insertar valores
cursor = connection.cursor()
cursor.executemany("""INSERT INTO auditoria VALUES (%s,%s,%s,%s,%s,%s,%s)""",chart)
connection.commit()
connection.close()