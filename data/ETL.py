import pandas as pd
import os 
# from transformers import GPT2Tokenizer, GPT2LMHeadModel
# import torch
# from torch.utils.data import Dataset, DataLoader
import tiktoken

def get_data(data_path, types):
    if not os.path.exists(data_path):
        raise FileExistsError(f"No se encuentra el archivo en {data_path}")
    
    column_names = {
        "users": {
            "id_user":"id usuario",
            "country":"pais",
            "degrees":"grados",
            "wage_aspiration":"aspiracion salarial",
            "currency":"moneda",
            "current_wage":"salario actual",
            "change_cities":"cambio ciudad",
            "language":"idioma",
            "years_experience":"años experiencia",
            "months_experience":"meses experiencia",
            "wish_role_name":"nombre cargo deseado",
            "work_modality":"modalidad de trabajo",
            "hardskills":"habilidades"
        },
        "vacancies": {
            "account executive":"id trabajo",
            "work_modality": "modalidad de trabajo",
            "country":"pais",
            "city":"ciudad",
            "remote":"remoto",
            "vacancy_name":"nombre vacante",
            "description":"descripcion"
        }
    }
    
    if types not in column_names:
        raise ValueError(f"Tipo desconocido: {types} los tipos válidos son:{list(column_names.keys())}")
    
    data = pd.read_csv(data_path)
    data = data.rename(columns=column_names[types])
    
    return data

def process_user_data(data):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    columns_to_drop = ["grados", "subareas", "salario actual", "cambio ciudad", "meses experiencia"]
    data = data.drop(columns=columns_to_drop)
    
    columns_to_check = ["años experiencia", "nombre cargo deseado", "habilidades"]
    data = data.dropna(subset=columns_to_check)
    data = data[["id usuario", "idioma", "aspiracion salarial", "idioma", "años experiencia", "nombre cargo deseado", "habilidades"]]
    
    return data

def process_vacancies_data(data):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    columns_to_check = ["id trabajo", "area", "pais", "ciudad"]
    data = data.dropna(subset=columns_to_check)
    
    return data
    

def get_jobs(data):
    assert "nombre vacante" in data, "nombre vacante no está en la base de datos"
    assert "descripcion" in data, "descripcion no está en la base de datos"
    

    # data["tokens"] = data.apply(lambda row: tokenizer.encode(row["nombre vacante"] + " " + row["descripcion"], truncation=True), axis=1)
    # data["num_tokens"] = data["tokens"].apply(len)
    
    # data = data[data["num_tokens"] <= 3000]

    jobs = data[["id trabajo","nombre vacante", "descripcion"]].to_dict("records")
    return jobs

def count_tokens(text):
    encoding = tiktoken.encoding_for_model("text-davinci-003")
    n_tokens = len(encoding.encode(text))
    return n_tokens
    
