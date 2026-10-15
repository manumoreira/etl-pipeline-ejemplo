import yaml
import random
import pandas as pd
from faker import Faker
import uuid

fake = Faker('es_AR')
NUM_RESPUESTAS = 150

def load_config(path='config/codebook.yml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def ensuciar_texto(texto):
    if random.random() < 0.15:
        texto = texto.lower()
    if random.random() < 0.20:
        texto = f"   {texto} "
    return texto

def ensuciar_edad(edad):
    rand = random.random()
    if rand < 0.05: return f"{edad} años"
    if rand < 0.10: return "treinta" 
    if rand < 0.15: return ""        
    return edad

def generate_mock_data():
    config = load_config()
    raw_columns = {v: k for k, v in config['column_mappings'].items()}
    
    data = []
    for _ in range(NUM_RESPUESTAS):
        genero = ensuciar_texto(random.choice(list(config['value_mappings']['genero'].keys())))
        educacion = ensuciar_texto(random.choice(list(config['value_mappings']['nivel_educativo'].keys())))
        economia = ensuciar_texto(random.choice(list(config['value_mappings']['evaluacion_economia'].keys())))
        direccion = ensuciar_texto(random.choice(list(config['value_mappings']['direccion_pais_acuerdo'].keys())))
        
        opciones_problemas = config['multiple_choice']['problemas_principales']['options']
        problemas = random.sample(opciones_problemas, k=random.randint(1, 3))
        if random.random() < 0.1:
            problemas.append(random.choice(["La corrupción ", " Todo está mal", "Ns/Nc"]))
        
        separador = ", " if random.random() > 0.5 else ","
        problemas_str = separador.join(problemas)

        sugerencia = fake.sentence() if random.random() > 0.3 else ""
        
        row = {
            raw_columns['id_encuesta']: str(uuid.uuid4())[:8],
            raw_columns['fecha_encuesta']: fake.date_time_between(start_date='-30d', end_date='now').strftime("%d/%m/%Y %H:%M:%S"),
            raw_columns['genero']: genero if random.random() > 0.05 else None,
            raw_columns['edad']: ensuciar_edad(random.randint(18, 85)),
            raw_columns['nivel_educativo']: educacion,
            raw_columns['evaluacion_economia']: economia,
            raw_columns['direccion_pais_acuerdo']: direccion,
            raw_columns['problemas_principales']: problemas_str,
            raw_columns['sugerencias_soluciones']: sugerencia
        }
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv('data/raw/encuesta_cruda.csv', index=False, encoding='utf-8')
    print(f"Generadas {NUM_RESPUESTAS} respuestas con ruido en 'data/raw/encuesta_cruda.csv'")

if __name__ == '__main__':
    generate_mock_data()