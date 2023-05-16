![Logo soy Henry](images/logo-henry-white-lg.png)

<h1 align="center"> PROYECTO INDIVIDUAL 01 </h1>

![Recomendación Peliculas](images/recommender-system-for-movie-recommendation.jpg)

<h2 align="center"> ¡Bienvenidos a mi repositorio con el proyecto de ETL, EDA y modelo de Machine Leaning para recomendar peliculas</h2>

### Descripción del problema

Se nos hizo entrega de un dataset llamado "movies_dataset.csv" del cual tuvimos que hacerle un proceso de ETL (Extract Transform and Load)<br>
De la cual se creo el archivo llamado "movies_dataset_clean.csv" para realizar las siguientes funciones: <br>
> Puede ver este proceso de manera detallada en el archivo llamado "ETL_part01.ipynb"
 - def peliculas_mes(mes): '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes (nombre del mes, en str, ejemplo 'enero') historicamente''' return {'mes':mes, 'cantidad':respuesta}

 - def peliculas_dia(dia): '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia (de la semana, en str, ejemplo 'lunes') historicamente''' return {'dia':dia, 'cantidad':respuesta}

 - def franquicia(franquicia): '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio''' return {'franquicia':franquicia, 'cantidad':respuesta, 'ganancia_total':respuesta, 'ganancia_promedio':respuesta}

 - def peliculas_pais(pais): '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo''' return {'pais':pais, 'cantidad':respuesta}

 - def productoras(productora): '''Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron''' return {'productora':productora, 'ganancia_total':respuesta, 'cantidad':respuesta}

 - def retorno(pelicula): '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo''' return {'pelicula':pelicula, 'inversion':respuesta, 'ganacia':respuesta,'retorno':respuesta, 'anio':respuesta}

### Desarrollando un Fastapi y luego subirlo a Render
Subiendolo al framework llamado FastAPI para construir un api y luego montandolo en la red con la aplicacion Render

### Procedemos a realizar el EDA (Exploratory data analysis)

> Creando el EDA en el archivo llamado EDA_part02.ipynb. <br> 

El EDA se realiza para comprender los datos y detectar patrones, anomalías y errores antes de realizar análisis más avanzados. <br>
Llegando a una matriz de correlación para ver cual columna es la más influyente y llegando a la conclusión de que datos tomaremos para armar nuestro modelo de machine learning.

### Creamos el sistema de recomendación

Llego la hora de entrenar nuestro modelo de machine learning para armar un sistema de recomendación de películas. <br>
Éste consiste en recomendar películas a los usuarios basándose en películas similares, por lo que se debe encontrar la similitud de puntuación entre esa película y el resto de películas, se ordenarán según el score de similaridad y devolverá una lista de Python con 5 valores, cada uno siendo el string del nombre de las películas con mayor puntaje, en orden descendente. <br>
> Puede ver nuestro modelo explicado en el archivo llamado "Modelo_part03.ipynb<br>

Usamos un promedio ponderado entre la columna vote_count y average_vote creando la columna "score"
Y luego ordenamos el dataframe por la columna "score" para quedarnos con las peliculas más aclamadas

### Corremos la función para recomendar peliculas
def recomendacion('titulo'): '''Ingresas un nombre de pelicula y te recomienda las similares en una lista de 5 valores''' return {'lista recomendada': respuesta}

### Proyecto 01 en Render [Link del Render](https://proyecto-individual-mauro.onrender.com/docs)
