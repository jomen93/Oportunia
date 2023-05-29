import pandas as pd
from data.ETL import get_data, process_user_data, get_jobs, process_vacancies_data
from config import configure_openai
import openai
import tiktoken
import re 

def generate_recommendations(user_ids):
    # Lectura de datos 
    data_users = get_data("data/users.csv", "users")
    data_vacancies = get_data("data/vacantes.csv", "vacancies")


    # Procesamiento de datos
    data_users = process_user_data(data_users)
    data_vacancies = process_vacancies_data(data_vacancies)
    user_ids = [154, 157, 159, 160, 163]


    openai.organization = "org-SiLCYY1CUhGJdlXvJAbvvUzf"
    openai.api_key = "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"

    max_tokens = 4096
    tokens_response = 200
    max_jobs = 0

    recomendations = pd.DataFrame()


    for user_id in user_ids:
        user = data_users[data_users["id usuario"] == user_id] 
        jobs = get_jobs(data_vacancies)[:40]

        for k in range(3):
            print(k)
            # Dividir los trabajos en grupos de n
            n = 2
            job_chunks = [jobs[i:i + n] for i in range(0, len(jobs), n)]
            top_job_chunk = []

            # Procesar cada grupo de trabajos
            for chunk in job_chunks:
                anos_experiencia = int(user['años experiencia'].values[0])
                nombre_cargo = user['nombre cargo deseado'].values[0].lower()
                habilidades = user['habilidades'].values[0].lower()
                idioma = ', '.join(user['idioma'].values[0])
                aspiracion_salarial = int(user["aspiracion salarial"].values[0])
                prompt = f"Soy alguien con {anos_experiencia} años de experiencia en {nombre_cargo} y tengo habilidades en {habilidades}, hablo {idioma}. Estoy buscando un trabajo con una aspiración salarial de {aspiracion_salarial}.\n\nAquí están algunas opciones de trabajo que estoy considerando:\n\n"
                for i, job in enumerate(chunk, start=1):
                    prompt += f"{int(job['id trabajo'])}. {job['nombre vacante']}:{job['descripcion']}\n"

                prompt += "\n¿lista de la mejor a peor las opcion mas adecuadas para mi con id de trabajo?"
                encoding = tiktoken.encoding_for_model("text-davinci-003")
                tokens = encoding.encode(prompt)
                n_tokens = len(encoding.encode(prompt)) + tokens_response
                print(f"tokens del prompt = {n_tokens}")

                response = openai.Completion.create(
                    engine = "text-davinci-003",
                    prompt = prompt,
                    temperature = 0.1,
                    max_tokens = tokens_response
                )

                # Procesar la respuesta y agregar la mejor opción a la lista de mejores trabajos
                best_option = response.choices[0].text.strip().split("\n")[0]
                best_option_name = best_option.split(". ")[1]  
                # print(best_option)
                top_job_chunk.append(best_option_name)

            # Imprimir los mejores trabajos
            top_job_chunk = [int(re.findall(r'\d{5}', i)[0]) for i in top_job_chunk]
            jobs = get_jobs(data_vacancies[data_vacancies["id trabajo"].isin(top_job_chunk)])
        
        recomendations_user = pd.DataFrame(jobs)
        recomendations_user["id usuario"] = user_id
        recomendations = pd.concat([recomendations, recomendations_user])
        
    recomendations.to_csv("data/recomendations.csv", index=False)