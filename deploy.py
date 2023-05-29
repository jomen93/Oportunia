from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Cargar las recomendaciones
recommendations = pd.read_csv("data/recomendations_score.csv")

@app.get('/recommendations/{user_id}')
async def get_recommendations(user_id: int):
    # Filtrar las recomendaciones para este usuario
    user_recommendations = recommendations[recommendations['id usuario'] == user_id]

    # Crear un diccionario donde las claves son los nombres de los trabajos y los valores son los puntajes
    jobs_and_scores = user_recommendations[['nombre vacante', 'match score']].set_index('nombre vacante').T.to_dict('records')[0]
    
    return jobs_and_scores

@app.get("/users")
async def get_users():
    # Devolver los usuarios únicos presentes en el dataframe
    unique_users = recommendations['id usuario'].unique().tolist()
    
    return unique_users
