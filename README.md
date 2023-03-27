<p align=center><img src=https://github.com/espadaone/PF_UCI-/blob/f25cddbc0242a77482c4124d631b4a2ce4654ab8/images/robotic-system-mobile-robots-help-work-workplace-servermobile-robot-help-communication.jpg><p>

# <h1 align=center> **DATA SCIENCE** </h1>

# <h1 align=center>**`Análisis de Acciones S&P500 y recomendaciones de inversión`**</h1>

<hr>  

¡A continuación se describirá los procesos de Extract, transform and load - ETL, Exploratory Data Analysis - EDA y Data Analytics llevados a cabo en el presente proyecto de ***Data Science***.  

<hr>

## Contexto
Cuando surgió la pandemia causada por el COVID-19, el mercado financiero internacional llevaba años de relativa tranquilidad posterior al desplome de 2008 con la burbuja de la deuda inmobiliaria estadounidense. La pandemia, un evento considerado por muchos analistas como un “cisne negro”, (sucesos que no habría habido forma alguna de predecir y con consecuencias graves), tuvo implicaciones trascendentales no sólo en la salud de las personas. Las medidas adoptadas por los gobiernos para afrontarla afectaron otros ámbitos, por ejemplo, los confinamientos cortaron por períodos más o menos extendidos casi todas las líneas de suministros perjudicando la producción global de bienes y servicios; o la generación de nuevas tendencias “remote first” llevaron al crecimiento exponencial de empresas de consumo masivo online o de herramientas que permitieran tal filosofía de trabajo, como Zoom.

Este cambio se tradujo en el mercado en un movimiento muy marcado de inversiones hacia empresas tecnológicas, mientras que las consideradas tradicionales se vieron más o menos desfavorecidas. Sin embargo, mucha gente dependiente de la presencialidad vio reducidos sus ingresos al punto de ver comprometida su subsistencia por lo que la mayoría de los gobiernos adoptó medidas de asistencia, recurriendo a la emisión monetaria para tales fines.

Esto llevó a una hiper liquidez a nivel global, cuyos efectos vemos aún al día de hoy: la Reserva Federal realiza hace tiempo aumentos de las tasas de interés que paga por sus bonos, a un ritmo no visto desde hace décadas, en un intento por bajar la aún creciente inflación. Esto, la incertidumbre con respecto a la situación económica mundial y el impacto de otros eventos como la guerra Ucrania-Rusia y el estrés que la misma salpicó a las relaciones geopolíticas internacionales, despertaron una migración al dólar estadounidense, en busca de refugio.

La suba de tasas por parte de la FED y la migración al dólar causaron su fortalecimiento, generando que muchos países en vías de desarrollo vieran encarecidas sus deudas en dólares, y empezaran a notarse indicios de una recesión inminente.

Los mercados financieros son el espacio en donde se encuentran la oferta y la demanda de activos financieros, como bonos y acciones. De esta forma, a través del mercado, los gobiernos y las empresas pueden obtener financiamiento mientras que las personas pueden invertir sus ahorros y obtener ganancias.

En líneas generales, en el corto/mediano plazo se observan muchas variaciones en los precios de los activos, pero a largo plazo se suelen observar tendencias alcistas (también llamadas bullish) o tendencias bajistas (bearish). Una herramienta utilizada para el correcto análisis y visualización de los precios, minimizando el “ruido” generado por la volatilidad inherente, son las medias móviles, que muestran el valor medio del precio de un mercado/activo durante un determinado período de tiempo y en función del cambio del precio, su valor medio va aumentando o disminuyendo.

Si por ejemplo tomamos una media móvil de periodo 200 (es decir, 200 sesiones) tenemos la media aritmética del precio durante las anteriores 200 sesiones y lo que se hace es que se suman los 200 precios de cierre y posteriormente los dividimos entre 200.

<hr>

## Objetivos

+ Extraer, transformar y cargar la data para ser analizada en un área de Analítica. 

+ Analizar los datos para encontrar relaciones, valores nulos, duplicados y otros

+ Desarrollar un Dashboard con indicadores para recomendar invertir en una empresa

<hr>  

# **I. ETL**

## 1. Extracción

Las `librerías` usadas son las siguientes: `pandas` para manejo de Dataframes, `datetime` para manejo de formatos fecha, `pandas_datareader` para leer data de yfinance e `yfinance` para acceder a la data de las acciones.

    import pandas as pd
    from datetime import
    from pandas_datareader
    import yfinance as yf

Posteriormente `scrapeamos` la información Wikipedia sobre las lista más prestigiosa de empresas que cotizan en bolsa `S&P500`. Para eso usamos el siguiente código:

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    SP500 = tables[0]
    SP500.head(1)

Una vez obtenido los valores del `S&P500` utilizamos la columna "Symbol" para scrapear la información existente desde el año 2000 hasta la fecha de `Acciones` mediante `yahoo`.

    today = datetime.today().date()
    today_pandas = pd.to_datetime(today)
    hoy=today_pandas.strftime('%Y-%m-%d')
    yf.pdr_override()
    data = pdr.get_data_yahoo(SP500_Symbol, start="2000-01-01", end=hoy)


<br/>

## 2. Transformación

En primer lugar, generamos una copia del DataFrame original y cambiamos el órden de su cabecera:

    data_aux=data.copy()
    data_aux.columns = data_aux.columns.swaplevel(0, 1)

En segundo lugar, mediante el siguiente código convertirmos al "index" Date en una columna.

    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data_aux.reset_index(inplace=True)
    data_aux['Date'] = pd.to_datetime(data_aux['Date'])

<br/>

## Carga

Esta etapara se ha realizado de manera directa debido que tanto el EDA como el ETL se han realizado en el mismo documento.

<br/>

# **II. EDA**

El siguiente Índice se ha utilizado para enfrentar el procesamiento EDA:

    1. IMPORTACIÓN DE LIBRERÍAS
    2. VISUALIZAMOS LA DATA
    3. LIMPIEZA DE DATOS
        3.1. Gestión de Nulos
        3.2. Gestión de Duplicados
        3.3. Gestión de Outliers
    4. SELECCIÓN DE NICHO
        4.1. Selección del Sector
            Análisis de Ratios de crecimiento
            Variación del precio en el tiempo
        4.2. Selección de 5 empresas con mejor rendimiento
    5. ANÁLISIS EXPLORATORIO
        5.1. Comportamiento Estadístico
    6. EXPORTAR DATA

A contunuación hay un breve resumen del desarrollo de cada sección del análisis EDA:

 <br/>

**1. IMPORTACIÓN DE `LIBRERÍAS`**

Las Librerías utilizadas son:

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

<br/>

**2. `VISUALIZAMOS` LA DATA**

La información está compuesta por una tabla de doble cabecera y para ser consultada se debe realizar en formato bidimensional.

<br/>

**3. `LIMPIEZA` DE DATOS**

*3.1. Gestión de `Nulos`*

Existen muchas empresas que están en la lista de las mejores 500 que han operado menos de 20 años, hay algunas empresas que tienen operaciones posterior al 2010. Esta información es clave al momento de comparar ratios y elegir la madurez de la compañía.

*3.2. Gestión de `Duplicados`*

Se ha medido la cantidad de duplicados y no existen dentro de la data. Por lo tanto, no se toma acción al respecto.

*3.3. Gestión de `Outliers`*

Los Outliers no fueron manipulados debido a que es data oficial de las acciones en el mundo y por ende ya fue procesada previamente.

<br/>

**4. SELECCIÓN DE `NICHO`**

*4.1. Selección del `Sector`*

En primer lugar para determinar el sector se ha considerado a los valores al cierre del día cómo precio de refencia, segundo se ha establecido promedios según el Años-MES.

    data_close=pd.DataFrame(data.loc[:,'Close'])     # Filtramos la Data en base al valor de cierre
    data_close['Date']=data.loc[:,'Date']            # Incluimos la columna Date
    data_close_anio_mes = data_close.groupby(
    data_close['Date'].dt.strftime('%Y-%m')).mean()  # Agrupar la data por Año-Mes

Se han analizado Análisis de `Ratios` de crecimiento y la `Variación` del precio en el tiempo. Este último es el insumo principal para anaizar el ratio de volatilidad.

*4.2. Selección de 5 empresas con mejor `rendimiento`*

Una vez seleccionada el sector por mejor tasa de crecimiento anualizada, procedemos a seleccionar las 5 empresas con mejor taza de crecimiento y mejor pendiente en su curva.

<br/>

**5. ANÁLISIS `EXPLORATORIO`**

En análisis exploratorio se ha centrado en una sola empresa con el fin de econtrar patrones o comportamientos que permitan entender mejor al dato.

    Acciones_AZO=pd.DataFrame(Acciones_aux.loc[:,'AZO'])     # Filtramos la Data por empresa
    Acciones_AZO                                             # Visualizamos

Una vez extraida la data correspondiente a la empresa "AZO" se ha graficado una curva sombreada con donde las zonas verdes indican cuando el valor de "OPEN" fue menor al valor de "CLOSE" por lo tanto durante el ´mes el promedio se tuvo un valor positivo y color rojo para el efecto opuesto. También se realizón un análisis de pairplot para encontrar relación lineal entre las variables.

*5.1. Comportamiento `Estadístico`*

La función *`.pct_change()`* permite calcular la variación de un precio respecto a su valor anterior. Luego de aplicar esta función, eliminanos los nulos residuales de la operación y graficamos para determinar si la media de las variables es distinta de 0.

<br/>

**6. `EXPORTAR` DATA**

Para exportar la data se ha realizado 2 grupos:

El primer grupo se exportaron los valores de las aciones por día y filtrado por el tipo de valor (ejemplo Close, Open,...). Estos valores son los mismos del dataframe original con la única excepción que solo incluye los valores de las empresas 5 empresas seleccionadas.

    Acciones["Close"].to_csv('Acciones_Close.csv', index=True)
    Acciones["Open"].to_csv('Acciones_Open.csv', index=True)
    Acciones["High"].to_csv('Acciones_High.csv', index=True)
    Acciones["Low"].to_csv('Acciones_Low.csv', index=True)
    Acciones["Volume"].to_csv('Acciones_Volume.csv', index=True)

En el grupo 2, se ha transformado la data del grupo 1 en especial la data de cierre "CLOSE". La función `.pct_change()` permite arrojar la variación de los precios respecto a su valor anterior.

    variacion_Close = Acciones['Close'].pct_change()
    variacion_Close.to_csv('variacion_Close.csv', index=True)

<br/>
<p align=center><img src=https://raw.githubusercontent.com/jamesllamo/SP500_Data_Analytics_Acciones/3bc131ce43711dd51afca84fc12ef02abad4d91d/src/17569089_57_MjYwNzIwIDE0.jpg><p>

<br/>
