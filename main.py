#Importación de las librerías necesarias.
from fastapi import FastAPI
import pandas as pd
import uvicorn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#Le doy a mi FastApi un título, una descripción y una versión.
# Load datasets

df = pd.read_csv("movies_dataset_clean.csv")
data = pd.read_csv("movies_dataset.csv")

# API structure

app = FastAPI()


#función para que reconozca mi servidor local

@app.get('/')
async def index():
    return {'API realizada por Mauro Pimentel'}

@app.get('/about/')
async def about():
    return {'Proyecto individual de la cohorte 10 de Data Science'}

# 1era función
meses = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12"
}

@app.get("/peliculas_mes/{mes}")

async def peliculas_mes(mes: str):
    '''Ingresa el nombre de un mes y te retorna la cantidad de peliculas estrenadas ese mes'''
    # Convertimos el nombre del mes a su número correspondiente
    mes_numero = meses.get(mes.lower())
    if mes_numero is None:
        return {"error": "Mes inválido"}
    
    # Filtramos el DataFrame para obtener solo las películas estrenadas en el mes indicado
    peliculas_mes = df[df['release_date'].str.contains(f"{mes_numero}-")]
    
    # Obtenemos la cantidad de películas y la devolvemos como respuesta
    cantidad_peliculas = len(peliculas_mes)
    return {"mes": mes, "cantidad de peliculas estrenadas en ese mes": cantidad_peliculas}

# 2da Función

@app.get('/peliculas_dia/{dia}')
def peliculas_dia(dia: str):
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia historicamente'''
    # Filtrar el DataFrame por el nombre del día ingresado
    peliculas_dia_df = df[df['nombre_dia'] == dia.lower()]
    # Contar cuántas filas hay en el nuevo DataFrame
    cantidad = len(peliculas_dia_df)
    return {'dia': dia, 'cantidad de peliculas que se estrenaron ese dia historicamente': cantidad}

# 3ra función

@app.get("/franquicia/{franquicia}")
async def franquicia(franquicia: str):
    '''Ingresa una franquicia y te devuelve la cantidad de peliculas, la ganancia total y la ganancia promedio'''
    # Filtramos el DataFrame para obtener solo las películas que pertenecen a la franquicia indicada
    peliculas_franquicia = df[df['belongs_to_collection'] == franquicia]
    
    # Obtenemos la cantidad de películas, la ganancia total y la ganancia promedio, y las devolvemos como respuesta
    cantidad_peliculas = len(peliculas_franquicia)
    ganancia_total = peliculas_franquicia['revenue'].sum()
    ganancia_promedio = peliculas_franquicia['revenue'].mean()
    
    return {"franquicia": franquicia, "cantidad": cantidad_peliculas, "ganancia_total": ganancia_total, "ganancia_promedio": ganancia_promedio}

#4ta funcion

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''
    # Filtrar el DataFrame por país de producción
    df["production_countries"] = df["production_countries"].fillna("")
    df_filtrado = df[df['production_countries'].apply(lambda x: pais in str(x))]
    
    # Contar el número de filas resultantes
    cantidad_peliculas = len(df_filtrado)
    
    return {'pais':pais, 'cantidad':cantidad_peliculas}

# 5ta funcion
@app.get('/productoras/{productora}')
def productoras(productora:str):
    '''Ingresas la productora, retornando la ganancia toal y la cantidad de peliculas que produjeron'''
    df["production_companies"] = df["production_companies"].fillna("")
    productora_df = df[df['production_companies'].apply(lambda x: productora in str(x))]

    ganancia_total = productora_df['revenue'].sum()

    cantidad = len(productora_df)
    return {'productora':productora, 'ganancia_total':ganancia_total, 'cantidad':cantidad}


# 6ta funcion
@app.get('/retorno/{pelicula}')
def retorno(pelicula:str):
    '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo'''
    pelicula_filtrada = df.query(f"title == '{pelicula}'")
    inversion = int(pelicula_filtrada['budget'].values[0])
    ganancia = int(pelicula_filtrada['revenue'].values[0]) - inversion
    retorno = float(pelicula_filtrada['return'].values[0])
    anio = str(pelicula_filtrada['release_year'].values[0])
    return {'pelicula': pelicula, 'inversion': inversion, 'ganancia': ganancia, 'retorno': retorno, 'anio': anio}

# 7ma funcion
data = data.drop_duplicates(subset = 'title')
C = data['vote_average'].mean()
m = data['vote_count'].quantile(0.90)
data = data.loc[data['vote_count'] >= m]
def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)
data['score'] = data.apply(weighted_rating, axis=1)
data = data.sort_values('score', ascending = False)
tfidf = TfidfVectorizer(stop_words='english')
data['overview'] = data['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(data['overview'])
tfidf.get_feature_names_out()
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
data.reset_index(drop = True, inplace = True)
index = pd.Series(data.index, index = data['title']).drop_duplicates()

# Creamos la función de recomendación

@app.get('/recomendacion/{titulo}') 
def recomendacion(titulo:str):
    '''Ingresa un Titulo y te devuelve una lista con 5 peliculas recomendadas'''
    local_cosine_sim = cosine_sim
    if titulo not in index:
        return "La película no se encuentra entre el 10% de las mejores películas. Intenta con una mejor!"

    idx = index[titulo]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    result = data['title'].iloc[movie_indices]
    return {"Lista recomendada": list(result)}