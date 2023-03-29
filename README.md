<p align=center><img src=https://github.com/espadaone/PF_UCI-/blob/d001d3245a72a4123a2a2b0d0a54eef342f06d47/images/Header.jpg><p>

# <h1 align=center> **DATA SCIENCE** </h1>

# <h1 align=center>**`EDA, ETL, ML y Dashboard de Datos de UCI`**</h1>

<hr>  

¡A continuación se describirá los procesos de Extract, transform and load - ETL, Exploratory Data Analysis - EDA, Machine Learning, Data WareHouse y Data Analytics llevados a cabo en el presente proyecto de ***Data Science*** para el área de ***UCI**** de un Hospital.

<hr>

## Contexto

Este informe presenta un análisis de los datos de 101 pacientes que han sido ingresados en el área de Cuidados Intensivos (UCI) del Hospital, generando un total de 130 registros. Los datos se recopilaron de 26 tablas que contienen información relevante, como estudios médicos realizados, prescripciones médicas y otros datos clínicos. Sin embargo, una de las tablas no posee información. La tabla con más registros es CHARTEVENTS, con 758,355 datos. Es importante destacar que las fechas presentadas en el conjunto de datos están enmascaradas y las fechas con años del siglo XIX (1800) corresponden a personas mayores de 89 años. La estacionalidad de las fechas de ingreso/egreso y eventos se preserva según el hemisferio norte (verano en el hemisferio norte es entre junio y septiembre).

<hr>

## Accesos Importantes

| Ver Dashboard en PowerBI: | Ver Dashboard en StreamLit: | Ver presentación Final: |
| --- | --- | --- |
| [![VER](images/bDashboard.png)](https://github.com/espadaone/PF_UCI-/blob/62bc1a743f77194d1c9027e303a588d1583edb1e/dashboard_powerbi.pbix) | [![VER](images/bstreamlit.png)](https://dash-uci.streamlit.app/) | [![VER](images/bPPT.png)](https://github.com/espadaone/PF_UCI-) |

## Objetivos

+ Facilitar el entendimiento de los datos, sobre el paciente y  los recursos
+ Mejorar la capacidad de toma de decisiones
+ Aplicar nuevas tecnologías al negocio

<hr>

## Alcance

`¿Qué SÍ incluye?`

+ Procesamiento y almacenamiento.
+ Generación de ratios e indicadores
+ Visualización de datos
+ Estimar tasas
 
`¿Qué NO incluye?`

+ Sugerencias de medicación
+ Administrar los recursos
+ Predicciones de supervivencia / mortalidad
+ Disponibilidad de recursos
+ Clasificación de pacientes

<hr>

## **I. MODELO ENTIDAD RELACIÓN**

El modelo ER de este proyecto se armó según las columnas claves de cada tabla y evitando la redundancia de las referencias. A más detalle se puede observar en la siguiente refresenteación:

<p align=center><img src=images/Entity_Relationship_Diagram.jpg><p>

`VER MODELO ENTIDAD RELACIÓN COMPLETO` 👇

[![VER](images/bER.png)](https://github.com/espadaone/PF_UCI-/blob/bd0624f0bc79de89466ceb253129db5476031245/Diccionario_datos_actualizado.pdf)

<br/>

# **III. DATA WAREHOUSE**

Para asegurar el éxito de este proyecto se ha utilizado diferentes herramientas tecnológicas que permiten ejecutar de la mejor manera el proyecto. Se ha empleado un conjunto de tecnologías que abarcan diferentes áreas. En cuanto a la gestión y comunicación, se han utilizado herramientas como Slack, Google Apps y Github. Para el desarrollo, se ha hecho uso de lenguajes de programación como Python, junto con librerías como Pandas y NumPy, y se han utilizado bases de datos como PostgreSQL y SQL Azure, alojado en la plataforma Microsoft Azure. En cuanto a la visualización de los resultados obtenidos, se han utilizado herramientas como Matplotlib, Streamlit y Power BI. Finalmente, para la creación de modelos de machine learning, se ha hecho uso de la popular librería SKlearn.

A continuación les mostramos un resumen del tecnológico:

<p align=center><img src=images/stack_tecnologico1.png><p>

Las herramientas más importantes para el desarrollo y análisis de datos de este proyecto son los siguientes. Microsoft Azure, Python, Power BI, Github y Slack. Microsoft Azure ofrece un entorno virtual que permite la escalabilidad de datos, mayor velocidad de procesamiento, reducción de costo de mantenimiento de servidor local, mayor seguridad y protección de datos. Python es esencial para el análisis exploratorio de datos, el proceso de Extracción, Transformación y Carga de datos, y la automatización de generación de archivos csv para que luego estén disponibles en la máquina virtual de Azure. Power BI es un servicio de análisis de datos de Microsoft que se enfoca en proporcionar visualizaciones interactivas y capacidades de inteligencia empresarial. Por otro lado, Github funciona como el repositorio del desarrollo del proyecto y control de versiones, mientras que Slack es el sistema de comunicación continua del equipo de trabajo.

<br/>

# **VI. PIPELINE Y WORKFLOW DE LA INFORMACIÓN**

Se cuenta con una fuente de datos que está compuesta por un total de 26 archivos `csv`, los cuales son cargados a un archivo de Python. Para la realización del proceso ETL, se utiliza la `librería de pandas` y una vez llevadas a cabo las transformaciones, se procede a validar los datos y comenzar con la carga de la información. Dicha carga se efectúa mediante la `librería de pymysql`, la cual se encarga de generar la conexión con la base de datos. Las tablas requeridas ya se encuentran cargadas en la base de datos y son llenadas conforme se ejecuta la carga, incluyendo la generación de las relaciones necesarias. Una vez terminado el proceso, la base de datos queda lista para ser subida a la `nube de Azure`. La automatización de ETL se realiza con `azure data factory studio` y se ejecuta diariamente a las 6 de la mañana, conectándose directamente con Azure. Por último, la data obtenida es consultada y consumida por los procesos de `visualización` y el modelo de `Machine Learning`.

<p align=center><img src=images/Pipeline3.png><p>

<br/>

# **V. ETL**

## **1. Extracción**

La información es recopilada desde archivos csv que son proporcionados por el hospital. Estos archivos son luego cargados en un archivo `.py` con la ayuda de la librería `pandas`, y se almacenan en un dataframe para su posterior transformación y carga.

## **2. Transformación**

Una vez extraida la data se realizaron las siguientes transformaciones:

`1. Cambiar formato de las columnas de fechas`

Las columnas que incluian fechas se cambió el formato de texto a datetime.

`2. Cambio de formato de medidas`

Una de las unidades de medida más vista en los datos fue “ml” y “mL”, significan lo mismo(mililitros), así que todo se transformo a “mL”, esto solo aplica a las unidades de medida escalares y no a las vectoriales.

`3. Reemplazar Nulos`

Todos los valores N\D =  No data (Para valores nulos en campos de texto) fueron reemplazados por "0” o promedios en caso de columnas numéricas.

Los campos donde el tipo de dato es datetime se dejó con nulos debido a que es en muchos casos completarlo con otros valores generan errores de registros.

`4. Eliminación de tablas`

La tabla 'NOTEEVENTS' no fue incluida en la base de datos ya que no contiene ningún dato.

`5. Replanteamiento de tablas`

Se elimina las columnas ('insurance','language', 'religion', 'marital_status', 'ethnicity') de la tabla ADMISSIONS y fueron colocadas en la tabla PATIENTS. Se llegó a la conclusión de que las columnas eliminadas estarían mejor introducidas en la tabla de pacientes.

`6. Reordenamiento de los nombres de las columnas`

Se estableció un nuevo órden de las columnas colocando la columna PK en la primera columna.

`7. Eliminación de columnas`

La columna “row_id” se eliminó de las tablas donde ya se contaba con PK y donde no se contaba se constituyó en la PK

`8. Se eliminan duplicados`

Se eliminan duplicados de las tablas que contaban con duplicados.


## **3. Carga**

El código ETL creado transforma cada dataset en una sentencia T-SQL (INSERT INTO…) para agregar los datos a las tablas en SQL en un solo movimiento. Para lograrlo se ha usado la siguiente librería:

    import pymysql

`Creación de Data Warehouse`

Como DBMS se utilizó MySQL workbench, todas las tablas fueron creadas utilizando T-SQL.

`Creación manual de BD en MySQL`

La BD lleva por nombre pf_uci  y está creada dentro de Mysql Workbench.

`Creación de tablas en MySQL`

La base de datos está conformada por 25 tablas. Cada tabla lleva los mismos nombres que los csv que fueron disponibilizados por el hospital. La tabla NOTEEVENTS no fue incluida en el armado de la base de datos ya que no es necesaria, se recomienda al cliente que deje de tomarla en cuenta o haga una modificación en los datos que está recabando. Se renombraron las columnas con el nombre row_id, el nuevo formato de nombre para esas columnas es el nombre correspondiente de la tabla más ( “_id”) en las tablas de hechos. Esta columna fue removida de las tablas de dimensiones.

`Asignación de PK y FK`

Una vez que los datos se han transformado, se pueden cargar en un destino deseado, como un archivo CSV o una base de datos. Las sentencias son construidas respetando las PK y FK, además de los formatos de las tablas.

`Automatización de tareas con azure data factory studio`

Finalmente, se ha automatizado el proceso ETL utilizando un programador de tareas o una herramienta de orquestación como azure data factory studio para ejecutar el pipeline ETL en intervalos regulares.


  <br/>

# **VI. KPIs y DASHBOARD**

`Tasa de readmisión`

La tasa de readmisión en UCI de un hospital se refiere al porcentaje de pacientes que han sido dados de alta de la unidad de cuidados intensivos (UCI) de un hospital y que han tenido que ser readmitidos en la UCI dentro de un período de tiempo determinado.

`Tasa de supervivencia`

La tasa de supervivencia en la unidad de cuidados intensivos (UCI) de un hospital se refiere a la proporción de pacientes que sobreviven a su estadía en la UCI. En otras palabras, es el porcentaje de pacientes que ingresan en la UCI y sobreviven a su enfermedad o lesión y son dados de alta del hospital.

`Tasa de mortalidad`

La tasa de mortalidad en UCI (Unidad de Cuidados Intensivos) de un hospital es el porcentaje de pacientes que fallecen mientras reciben atención médica en la UCI de ese hospital. Esta tasa se calcula dividiendo el número de pacientes que fallecieron en la UCI por el número total de pacientes atendidos en la UCI durante un período de tiempo determinado, generalmente un año.

`Tasa de Pacientes con seguro privado`

La "tasa de pacientes con seguro privado en UCI de un hospital" se refiere a la proporción de pacientes que son admitidos en la unidad de cuidados intensivos (UCI) de un hospital y que tienen un seguro de salud privado en comparación con aquellos que tienen un seguro de salud público o no tienen seguro de salud en absoluto.

`Tasa cancelación de procedimientos`

La tasa de cancelación de procedimientos en una Unidad de Cuidados Intensivos (UCI) de un hospital se refiere a la proporción de procedimientos programados que se cancelan antes de su realización. Estos procedimientos pueden incluir cirugías, intervenciones invasivas, pruebas diagnósticas y otros procedimientos que se planifican para el cuidado de pacientes críticos en la UCI.

`Duración media de estancia en el hospital`

La duración media de estancia en el hospital en UCI (Unidad de Cuidados Intensivos) se refiere al tiempo promedio que los pacientes pasan en la UCI antes de ser dados de alta o trasladados a otra área del hospital. Es un indicador importante de la eficacia del tratamiento y la atención en la UCI, ya que una estancia prolongada en la UCI puede indicar complicaciones médicas o una recuperación lenta.

A continuación dejamos el acceso al Dashboard.

  <br/>

# **VII. MODELO DE MACHINE LEARNING**

Para la elaboración del modelo de Machine Learning se ha usado data las siguientes tablas: admissions, patients y prescriptions. Con esta data se ha realizado la predicción de estadía de los pacientes. Para la graficación de los resultados se ha dividido la predicciones en rangos etarios de: '<= 30 años', '30 a 49 años', '50 a 64 años', '65 a 79 años' y '>= 80 años'. El resultado de predicción se actualiza en tiempo real. A continuación mostraremos una visualización previa de los resultados.

<p align=center><img src=images/predicciones.jpg><p>

La predicción de la estadía de los pacientes en el área de UCI de un hospital puede tener varios usos importantes. Algunos de ellos son:

1. Planificación y gestión de recursos: Los hospitales pueden utilizar los resultados de la predicción para planificar y gestionar sus recursos de manera más efectiva. Por ejemplo, pueden asignar personal adicional en la UCI cuando se espera que la estadía de los pacientes sea más larga de lo habitual, o pueden reservar camas en la UCI para pacientes que se espera que requieran atención intensiva durante un período más prolongado.

2. Asignación de recursos médicos: La predicción de la estadía de los pacientes en la UCI también puede ayudar a los médicos a tomar decisiones más informadas sobre la asignación de recursos médicos. Por ejemplo, pueden decidir cuánto tiempo deben permanecer los pacientes en ventilación mecánica o cuándo pueden ser transferidos a unidades de cuidados menos intensivos.

3. Reducción de costos: La predicción de la estadía de los pacientes en la UCI también puede ayudar a los hospitales a reducir costos innecesarios. Por ejemplo, pueden evitar la sobreutilización de recursos médicos y reducir la duración de la estadía de los pacientes en la UCI cuando no es necesaria.

4. Mejora de la calidad de atención: Al predecir la estadía de los pacientes en la UCI, los hospitales pueden garantizar que los pacientes reciban la atención adecuada durante todo el tiempo que estén en la UCI. Esto puede mejorar la calidad de atención que se brinda a los pacientes, lo que puede llevar a mejores resultados de salud y a una mayor satisfacción del paciente.

<br/>

<p align=center><img src=https://github.com/espadaone/PF_UCI-/blob/c31c4bbdec1a6725a0daae09bac0b100a64608da/images/banner%20inferior.png><p>

<br/>
