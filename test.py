import pandas as pd
from data.ETL import get_data, process_user_data, process_vacancies_data
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

# Lectura de datos 
data_users = get_data("data/users.csv", "users")
data_vacancies = get_data("data/vacantes.csv", "vacancies")
recomendations = pd.read_csv("data/recomendations.csv")


# Procesamiento de datos
data_users = process_user_data(data_users)
data_vacancies = process_vacancies_data(data_vacancies)

# Se carga el BERT multilingue
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
model = AutoModel.from_pretrained("bert-base-multilingual-cased")

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs[0].mean(1).detach().numpy()
    return embeddings

# Generacion de embeddings para el perfil de los usuarios
user_profiles = data_users.set_index("id usuario").loc[recomendations["id usuario"].unique(), "habilidades"].apply(get_bert_embeddings)

# Generación embeddings para las descripciones de los trabajos
job_descriptions = recomendations["descripcion"].apply(get_bert_embeddings)

# Calculo de la similitud del coseno
match_scores = [cosine_similarity(user_profiles.loc[user_id].reshape(1, -1), job_desc.reshape(1, -1))[0][0] for user_id, job_desc in zip(recomendations['id usuario'], job_descriptions)]

print(match_scores)


recomendations["match score"] = match_scores
recomendations.to_csv("data/recomendations_score.csv", index=False)
